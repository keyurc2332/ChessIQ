# backend/routes/prediction.py - CORRECTED (Fixed 422 Error)

from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import User, Game
from database import get_db
from auth import decode_access_token
import pickle
import os
import numpy as np

router = APIRouter(prefix="/prediction", tags=["prediction"])

# Load trained model
MODEL_PATH = "chessiq_model.pkl"
METADATA_PATH = "chessiq_model_metadata.pkl"

model = None
metadata = None


# ============================================================================
# PYDANTIC MODELS (For Request/Response validation)
# ============================================================================

class PredictGameRequest(BaseModel):
    """Request body for game prediction"""
    player_rating: int
    opponent_rating: int
    time_control: str = "600"
    opening_eco: str = "A00"
    accuracy: float = 60.0
    avg_centipawn_loss: float = 100.0
    player_color: str = "white"


class PredictionResponse(BaseModel):
    """Response for prediction"""
    status: str
    prediction: str
    confidence: float
    win_probability: float
    loss_probability: float
    game_context: dict


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def load_model():
    """Load ML model from disk"""
    global model, metadata
    
    if model is None:
        try:
            if os.path.exists(MODEL_PATH):
                with open(MODEL_PATH, 'rb') as f:
                    model = pickle.load(f)
                print(f"✅ Model loaded: {MODEL_PATH}")
            else:
                print(f"⚠️  Model not found at {MODEL_PATH}")
                print("   Run: python ml_pipeline.py")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
    
    if metadata is None:
        try:
            if os.path.exists(METADATA_PATH):
                with open(METADATA_PATH, 'rb') as f:
                    metadata = pickle.load(f)
            else:
                print(f"⚠️  Metadata not found at {METADATA_PATH}")
        except Exception as e:
            print(f"❌ Error loading metadata: {e}")
    
    return model is not None


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


def encode_time_control(tc):
    """Convert time control to category"""
    try:
        tc_int = int(tc)
        if tc_int <= 60:
            return 0  # bullet
        elif tc_int <= 600:
            return 1  # blitz
        else:
            return 2  # rapid
    except:
        return 1


def encode_opening(eco):
    """Convert ECO to opening category"""
    if not eco or eco == 'A00':
        opening = 'Other'
    else:
        first_letter = eco[0]
        if first_letter in ['A', 'B']:
            opening = 'Flank'
        elif first_letter == 'C':
            opening = 'Open Game'
        elif first_letter == 'D':
            opening = 'Closed Game'
        else:
            opening = 'Other'
    
    # Encode opening category
    opening_map = {'Flank': 0, 'Open Game': 1, 'Closed Game': 2, 'Other': 3}
    return opening_map.get(opening, 3)


# ============================================================================
# API ENDPOINTS
# ============================================================================

@router.post("/predict-game")
def predict_game(
    request: PredictGameRequest,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Predict win/loss probability for a game"""
    
    # Load model if not already loaded
    if not load_model():
        raise HTTPException(
            status_code=503,
            detail="Model not available. Run 'python ml_pipeline.py' first."
        )
    
    try:
        # Prepare features
        rating_diff = request.player_rating - request.opponent_rating
        time_encoded = encode_time_control(request.time_control)
        opening_encoded = encode_opening(request.opening_eco)
        player_color_encoded = 1 if request.player_color == "white" else 0
        
        # Feature vector (must match training features order)
        features = np.array([[
            request.player_rating,
            request.opponent_rating,
            rating_diff,
            request.accuracy,
            request.avg_centipawn_loss,
            time_encoded,
            opening_encoded,
            player_color_encoded
        ]])
        
        # Get prediction and probability
        prediction = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]
        
        win_prob = probabilities[1] * 100
        loss_prob = probabilities[0] * 100
        
        prediction_text = "WIN" if prediction == 1 else "LOSS"
        
        return {
            "status": "success",
            "prediction": prediction_text,
            "confidence": round(win_prob, 2),
            "win_probability": round(win_prob, 2),
            "loss_probability": round(loss_prob, 2),
            "game_context": {
                "your_rating": request.player_rating,
                "opponent_rating": request.opponent_rating,
                "rating_difference": rating_diff,
                "time_control": request.time_control,
                "opening": request.opening_eco,
                "your_accuracy_avg": request.accuracy,
                "your_cpl_avg": request.avg_centipawn_loss
            }
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {str(e)}"
        )


@router.get("/model-info")
def get_model_info(
    current_user: User = Depends(get_current_user_from_header)
):
    """Get information about the trained model"""
    
    if not load_model() or metadata is None:
        raise HTTPException(
            status_code=503,
            detail="Model not available"
        )
    
    try:
        feature_importance = metadata.get('feature_importance')
        
        importance_list = []
        if feature_importance is not None:
            for idx, row in feature_importance.iterrows():
                importance_list.append({
                    "feature": row['feature'],
                    "importance": round(float(row['importance']), 4)
                })
        
        return {
            "status": "success",
            "model_info": {
                "type": metadata.get('model_type', 'XGBClassifier'),
                "trained_at": metadata.get('trained_at'),
                "features": metadata.get('features', []),
                "feature_count": len(metadata.get('features', [])),
                "feature_importance": importance_list[:10]  # Top 10
            }
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving model info: {str(e)}"
        )


@router.post("/predict-upcoming-games")
def predict_upcoming_games(
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Predict win probability for user's next 10 games based on patterns"""
    
    if not load_model():
        raise HTTPException(
            status_code=503,
            detail="Model not available"
        )
    
    try:
        # Get user's last 10 games
        recent_games = db.query(Game).filter(
            Game.user_id == current_user.user_id
        ).order_by(Game.played_at.desc()).limit(10).all()
        
        if not recent_games:
            raise HTTPException(
                status_code=400,
                detail="No games found for prediction"
            )
        
        # Calculate average stats
        avg_rating = np.mean([g.player_rating_before or 1200 for g in recent_games])
        avg_opponent = np.mean([g.opponent_rating or 1200 for g in recent_games])
        avg_accuracy = np.mean([g.accuracy or 60 for g in recent_games])
        avg_cpl = np.mean([g.avg_centipawn_loss or 100 for g in recent_games])
        
        # Get most common time control
        time_controls = [g.time_control for g in recent_games if g.time_control]
        time_control = max(set(time_controls), key=time_controls.count) if time_controls else "600"
        
        # Predict for upcoming games
        predictions = []
        for i in range(5):
            # Vary opponent rating slightly
            opp_rating = avg_opponent + np.random.randint(-100, 100)
            
            features = np.array([[
                avg_rating,
                opp_rating,
                avg_rating - opp_rating,
                avg_accuracy,
                avg_cpl,
                encode_time_control(time_control),
                encode_opening("A00"),
                1  # Assume white
            ]])
            
            prob = model.predict_proba(features)[0][1] * 100
            
            predictions.append({
                "game_number": i + 1,
                "predicted_opponent_rating": int(opp_rating),
                "win_probability": round(prob, 2),
                "prediction": "WIN" if prob > 50 else "LOSS"
            })
        
        return {
            "status": "success",
            "your_average_stats": {
                "rating": round(avg_rating, 0),
                "opponent_rating": round(avg_opponent, 0),
                "accuracy": round(avg_accuracy, 2),
                "cpl": round(avg_cpl, 2)
            },
            "predicted_upcoming_games": predictions
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error predicting games: {str(e)}"
        )