# backend/schemas.py - COMPLETE VERSION

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserRegister(BaseModel):
    """User registration schema"""
    email: EmailStr
    password: str
    chess_com_username: Optional[str] = None
    lichess_username: Optional[str] = None


class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User response schema"""
    user_id: str
    email: str
    chess_com_username: Optional[str] = None
    lichess_username: Optional[str] = None
    created_at: datetime


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str
    user: UserResponse


class GameResponse(BaseModel):
    """Game response schema"""
    game_id: str
    opponent: str
    result: str
    played_at: datetime
    opening: str
    time_control: str
    accuracy: Optional[float] = None
    is_analyzed: bool


class AnalysisResponse(BaseModel):
    """Analysis response schema"""
    game_id: str
    accuracy: float
    avg_cpl: float
    moves_analyzed: int


class GameSummaryResponse(BaseModel):
    """Game summary response schema"""
    total_games: int
    wins: int
    losses: int
    draws: int
    win_rate: float
    avg_accuracy: float