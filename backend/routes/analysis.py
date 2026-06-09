# backend/routes/analysis.py - PROPER PARALLEL VERSION with Independent Sessions

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from models import User, Game, Move
from database import get_db, SessionLocal
from auth import decode_access_token
from stockfish_analyzer import StockfishAnalyzer
from concurrent.futures import ThreadPoolExecutor, as_completed
import uuid

router = APIRouter(prefix="/analysis", tags=["analysis"])

MAX_WORKERS = 4  # Back to 4 parallel workers!


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


def analyze_single_game_with_session(game_id, moves_pgn, player_color):
    """
    Analyze a single game with its OWN database session
    This prevents concurrent session conflicts!
    """
    try:
        # Create a NEW session for THIS worker
        db = SessionLocal()
        
        # Get the game
        game = db.query(Game).filter(Game.game_id == game_id).first()
        if not game:
            db.close()
            return {"game_id": game_id, "status": "not_found"}
        
        # Analyze with Stockfish
        analyzer = StockfishAnalyzer(depth=15)
        result = analyzer.analyze_pgn_moves(moves_pgn, player_color)
        
        if result:
            # Update game
            game.is_analyzed = 1
            game.accuracy = result["accuracy"]
            game.avg_centipawn_loss = result["avg_cpl"]
            
            # Store moves
            for move_data in result.get("analyses", []):
                move_record = Move(
                    game_id=game.game_id,
                    move_number=move_data["move_number"],
                    move_san=move_data["move_san"],
                    move_uci=move_data["move"],
                    eval_before=move_data["evaluation_before"],
                    eval_after=move_data["evaluation_after"],
                    centipawn_loss=move_data["centipawn_loss"]
                )
                db.add(move_record)
            
            db.commit()
            db.close()
            
            return {
                "game_id": game_id,
                "status": "success",
                "accuracy": result["accuracy"],
                "avg_cpl": result["avg_cpl"],
                "moves_count": len(result.get("analyses", []))
            }
        else:
            db.close()
            return {"game_id": game_id, "status": "analysis_failed"}
    
    except Exception as e:
        try:
            db.rollback()
            db.close()
        except:
            pass
        return {
            "game_id": game_id,
            "status": "error",
            "error": str(e)[:50]
        }


@router.post("/batch/all-unanalyzed")
def analyze_all_unanalyzed(
    db: Session = Depends(get_db)
):
    """
    Fast parallel batch analysis with independent sessions
    - 4 parallel workers (each with own database session)
    - Depth=15 (maximum accuracy)
    - NO concurrent session conflicts!
    """
    
    try:
        unanalyzed = db.query(Game).filter(
            Game.is_analyzed == 0
        ).all()
        
        total_games = len(unanalyzed)
        print(f"\n📊 Starting analysis of {total_games} games...")
        print(f"⚡ Using {MAX_WORKERS} parallel workers (independent sessions)")
        print(f"🎯 Depth: 15 (MAXIMUM ACCURACY)\n")
        
        analyzed_count = 0
        moves_stored = 0
        errors = 0
        
        # Prepare game data for workers
        games_data = [
            (game.game_id, game.moves, game.player_color)
            for game in unanalyzed
        ]
        
        # Parallel processing with independent sessions
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {
                executor.submit(analyze_single_game_with_session, game_id, moves, color): (game_id, i)
                for i, (game_id, moves, color) in enumerate(games_data)
            }
            
            for future in as_completed(futures):
                try:
                    result = future.result()
                    game_id, idx = futures[future]
                    
                    if result["status"] == "success":
                        analyzed_count += 1
                        moves_stored += result.get("moves_count", 0)
                        
                        if analyzed_count % 50 == 0:
                            print(f"  ✅ Analyzed {analyzed_count}/{total_games} games... ({moves_stored} moves stored)")
                    
                    elif result["status"] == "error":
                        errors += 1
                
                except Exception as e:
                    errors += 1
                    print(f"  ❌ Worker error: {str(e)[:50]}")
        
        print(f"\n✅ Analysis Complete!")
        print(f"   Games analyzed: {analyzed_count}/{total_games}")
        print(f"   Moves stored: {moves_stored}")
        print(f"   Errors: {errors}")
        print(f"   Accuracy level: MAXIMUM (Depth 15)")
        
        return {
            "status": "success",
            "message": f"Analyzed {analyzed_count} games in parallel",
            "total": total_games,
            "analyzed": analyzed_count,
            "games_analyzed": analyzed_count,
            "moves_analyzed": moves_stored
        }
    
    except Exception as e:
        print(f"Error in batch analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))