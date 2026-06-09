# backend/routes/games.py - CORRECTED VERSION (No Dedup Issue)

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Header
from sqlalchemy.orm import Session
from models import User, Game
from database import get_db
from auth import decode_access_token
from pgn_parser import parse_pgn_file
import uuid
import hashlib

router = APIRouter(prefix="/games", tags=["games"])


def get_current_user_from_header(authorization: str = Header(None), db: Session = Depends(get_db)):
    """Extract user from Authorization header"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        token = authorization.split(" ")[1]
        user_id = decode_access_token(token)
        user = db.query(User).filter(User.user_id == user_id).first()
        
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/upload_pgn")
async def upload_pgn(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Upload and parse PGN file with improved error handling"""
    
    try:
        # Read file content
        content = await file.read()
        pgn_text = content.decode('utf-8', errors='ignore')
        
        if not pgn_text.strip():
            raise HTTPException(
                status_code=400,
                detail="File is empty"
            )
        
        print(f"\n📥 Processing PGN file ({len(pgn_text) / 1024 / 1024:.2f} MB)...")
        
        # Use improved parser that handles corrupted games
        games_data = parse_pgn_file(pgn_text)
        
        if not games_data:
            return {
                "status": "error",
                "message": "No valid games found in file"
            }
        
        print(f"✅ Parsed {len(games_data)} valid games\n")
        
        imported_count = 0
        skipped_count = 0
        
        # Store games in database
        for i, game_data in enumerate(games_data):
            try:
                # Create hash for deduplication (but don't check it)
                game_hash = hashlib.md5(
                    f"{game_data['moves']}{game_data['played_at']}".encode()
                ).hexdigest()
                
                # Determine player color (assume user is White)
                player_color = "white"
                opponent = game_data['black_player']
                opponent_rating = game_data['black_elo']
                player_rating = game_data['white_elo']
                result = game_data['result']
                
                # Create game record
                new_game = Game(
                    game_id=str(uuid.uuid4()),
                    user_id=current_user.user_id,
                    played_at=game_data['played_at'],
                    source="chess_com_import",
                    source_game_id=game_hash,
                    player_color=player_color,
                    player_rating_before=player_rating,
                    opponent_username=opponent,
                    opponent_rating=opponent_rating,
                    time_control=game_data['time_control'],
                    opening_eco=game_data['opening_eco'],
                    opening_name=game_data['opening_name'],
                    result=result,
                    moves=game_data['moves'],
                    is_analyzed=0
                )
                
                db.add(new_game)
                imported_count += 1
                
                if (i + 1) % 500 == 0:
                    db.commit()
                    print(f"  💾 Saved {imported_count} games...")
            
            except Exception as e:
                skipped_count += 1
                continue
        
        db.commit()
        
        print(f"\n✅ Import complete!")
        print(f"   Imported: {imported_count}")
        print(f"   Skipped: {skipped_count}")
        
        return {
            "status": "success",
            "games_imported": imported_count,
            "games_skipped": skipped_count,
            "total_processed": imported_count + skipped_count,
            "message": f"Imported {imported_count} games from Chess.com"
        }
    
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )


@router.get("/list")
def get_games_list(
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Get list of user's games"""
    
    games = db.query(Game).filter(Game.user_id == current_user.user_id).all()
    
    return {
        "status": "success",
        "total_games": len(games),
        "games": [
            {
                "game_id": g.game_id,
                "played_at": g.played_at,
                "opponent": g.opponent_username,
                "result": g.result,
                "opening": g.opening_name or g.opening_eco,
                "time_control": g.time_control,
                "is_analyzed": bool(g.is_analyzed),
                "accuracy": g.accuracy
            }
            for g in sorted(games, key=lambda x: x.played_at, reverse=True)
        ]
    }


@router.get("/summary")
def get_games_summary(
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Get summary statistics of user's games"""
    
    games = db.query(Game).filter(Game.user_id == current_user.user_id).all()
    
    if not games:
        return {
            "status": "success",
            "total_games": 0,
            "wins": 0,
            "losses": 0,
            "draws": 0,
            "win_rate": 0,
            "avg_accuracy": 0
        }
    
    wins = sum(1 for g in games if g.result == "win")
    losses = sum(1 for g in games if g.result == "loss")
    draws = sum(1 for g in games if g.result == "draw")
    
    accuracies = [g.accuracy for g in games if g.accuracy is not None]
    avg_accuracy = sum(accuracies) / len(accuracies) if accuracies else 0
    
    win_rate = (wins / len(games) * 100) if games else 0
    
    return {
        "status": "success",
        "total_games": len(games),
        "wins": wins,
        "losses": losses,
        "draws": draws,
        "win_rate": round(win_rate, 2),
        "avg_accuracy": round(avg_accuracy, 2),
        "analyzed_games": sum(1 for g in games if g.is_analyzed)
    }