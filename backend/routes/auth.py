# backend/routes/auth.py - COMPLETE VERSION

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from models import User
from schemas import UserRegister, UserLogin, TokenResponse, UserResponse
from database import get_db
from auth import hash_password, verify_password, create_access_token, decode_access_token
import uuid

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=TokenResponse)
def signup(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user"""
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user_id = str(uuid.uuid4())
    hashed_password = hash_password(user_data.password)
    
    new_user = User(
        user_id=user_id,
        email=user_data.email,
        password_hash=hashed_password,
        chess_com_username=user_data.chess_com_username,
        lichess_username=user_data.lichess_username
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create token
    token = create_access_token(user_id)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "user_id": new_user.user_id,
            "email": new_user.email
        }
    }


@router.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    
    # Find user by email
    user = db.query(User).filter(User.email == user_data.email).first()
    
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create token
    token = create_access_token(user.user_id)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "user_id": user.user_id,
            "email": user.email
        }
    }


@router.get("/me", response_model=UserResponse)
def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    """Get current user info"""
    
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    try:
        # Extract token from "Bearer <token>"
        token = authorization.split(" ")[1]
        user_id = decode_access_token(token)
        
        user = db.query(User).filter(User.user_id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        return {
            "user_id": user.user_id,
            "email": user.email,
            "chess_com_username": user.chess_com_username,
            "lichess_username": user.lichess_username,
            "created_at": user.created_at
        }
    
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )