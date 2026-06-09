# backend/ml_pipeline.py - COMPLETE ML PIPELINE
# Feature Engineering + XGBoost Training + SHAP Explainability

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
import shap
import pickle
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Game, User
from dotenv import load_dotenv

# Load environment
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/chessiq")

print("="*70)
print("ChessIQ - XGBoost Win Prediction ML Pipeline")
print("="*70)

# ============================================================================
# STEP 1: LOAD DATA FROM DATABASE
# ============================================================================

def load_games_from_db():
    """Load all analyzed games from database"""
    print("\n📥 Loading games from database...")
    
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # Get all analyzed games
        games = db.query(Game).filter(Game.is_analyzed == 1).all()
        
        if not games:
            print("❌ No analyzed games found!")
            return None
        
        print(f"✅ Loaded {len(games)} analyzed games")
        
        # Convert to list of dicts
        games_data = []
        for g in games:
            games_data.append({
                'game_id': g.game_id,
                'player_rating': g.player_rating_before or 1200,
                'opponent_rating': g.opponent_rating or 1200,
                'time_control': g.time_control or '600',
                'opening_eco': g.opening_eco or 'A00',
                'accuracy': g.accuracy or 50.0,
                'avg_centipawn_loss': g.avg_centipawn_loss or 100.0,
                'result': 1 if g.result == 'win' else (0 if g.result == 'loss' else 0.5),
                'player_color': 1 if g.player_color == 'white' else 0,
            })
        
        db.close()
        return games_data
    
    except Exception as e:
        print(f"❌ Error loading games: {e}")
        db.close()
        return None


# ============================================================================
# STEP 2: FEATURE ENGINEERING
# ============================================================================

def engineer_features(games_data):
    """Create features for ML model"""
    print("\n🔧 Engineering features...")
    
    df = pd.DataFrame(games_data)
    
    # Calculate rating difference
    df['rating_diff'] = df['player_rating'] - df['opponent_rating']
    
    # Extract time control type
    def get_time_control_category(tc):
        try:
            tc_int = int(tc)
            if tc_int <= 60:
                return 'bullet'  # 0
            elif tc_int <= 600:
                return 'blitz'   # 1
            else:
                return 'rapid'   # 2
        except:
            return 'blitz'
    
    df['time_category'] = df['time_control'].apply(get_time_control_category)
    
    # Encode time control
    time_encoder = {'bullet': 0, 'blitz': 1, 'rapid': 2}
    df['time_encoded'] = df['time_category'].map(time_encoder)
    
    # Extract opening type from ECO
    def get_opening_category(eco):
        if not eco or eco == 'A00':
            return 'Other'
        first_letter = eco[0]
        if first_letter in ['A', 'B']:
            return 'Flank'
        elif first_letter == 'C':
            return 'Open Game'
        elif first_letter == 'D':
            return 'Closed Game'
        else:
            return 'Other'
    
    df['opening_category'] = df['opening_eco'].apply(get_opening_category)
    
    # Encode opening
    opening_encoder = LabelEncoder()
    df['opening_encoded'] = opening_encoder.fit_transform(df['opening_category'])
    
    # Target variable (1 = win, 0 = loss/draw)
    df['target'] = (df['result'] == 1).astype(int)
    
    # Select features
    features = ['player_rating', 'opponent_rating', 'rating_diff', 'accuracy', 
                'avg_centipawn_loss', 'time_encoded', 'opening_encoded', 'player_color']
    
    X = df[features]
    y = df['target']
    
    print(f"✅ Features engineered:")
    print(f"   - Samples: {len(X)}")
    print(f"   - Features: {len(features)}")
    print(f"   - Win rate in data: {y.mean()*100:.1f}%")
    
    return X, y, features, df


# ============================================================================
# STEP 3: TRAIN XGBOOST MODEL
# ============================================================================

def train_xgboost_model(X, y, features):
    """Train XGBoost classifier"""
    print("\n🤖 Training XGBoost model...")
    
    # Split data: 80% train, 20% test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"   Train set: {len(X_train)} games")
    print(f"   Test set: {len(X_test)} games")
    
    # Create and train model
    model = xgb.XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric='logloss',
        verbosity=0
    )
    
    # Train with validation
    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        verbose=False
    )
    
    # Evaluate
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    print(f"\n✅ Model trained!")
    print(f"   Train accuracy: {train_score*100:.2f}%")
    print(f"   Test accuracy: {test_score*100:.2f}%")
    
    return model, X_train, X_test, y_train, y_test, features


# ============================================================================
# STEP 4: SHAP EXPLAINABILITY
# ============================================================================

def generate_shap_explanations(model, X_train, X_test, features):
    """Generate SHAP feature importance"""
    print("\n📊 Generating SHAP explanations...")
    
    try:
        # Create explainer
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_test)
        
        # Get feature importance
        if isinstance(shap_values, list):
            shap_values = shap_values[1]  # For binary classification
        
        feature_importance = np.abs(shap_values).mean(axis=0)
        
        # Create importance dataframe
        importance_df = pd.DataFrame({
            'feature': features,
            'importance': feature_importance
        }).sort_values('importance', ascending=False)
        
        print(f"\n✅ SHAP Analysis Complete!")
        print("\nTop 5 Most Important Features:")
        for idx, row in importance_df.head(5).iterrows():
            print(f"   {idx+1}. {row['feature']}: {row['importance']:.4f}")
        
        return importance_df, explainer, shap_values
    
    except Exception as e:
        print(f"⚠️  SHAP generation issue (non-critical): {e}")
        return None, None, None


# ============================================================================
# STEP 5: SAVE MODEL
# ============================================================================

def save_model(model, importance_df, features):
    """Save trained model and metadata"""
    print("\n💾 Saving model...")
    
    model_path = "chessiq_model.pkl"
    metadata_path = "chessiq_model_metadata.pkl"
    
    # Save model
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"   ✅ Model saved: {model_path}")
    
    # Save metadata
    metadata = {
        'features': features,
        'feature_importance': importance_df,
        'trained_at': datetime.now().isoformat(),
        'model_type': 'XGBClassifier',
        'test_accuracy': model.score.__doc__
    }
    
    with open(metadata_path, 'wb') as f:
        pickle.dump(metadata, f)
    print(f"   ✅ Metadata saved: {metadata_path}")
    
    return model_path, metadata_path


# ============================================================================
# STEP 6: GENERATE PREDICTIONS
# ============================================================================

def generate_sample_predictions(model, df, features):
    """Generate sample predictions on test data"""
    print("\n🎯 Sample Predictions:")
    
    X = df[features]
    
    # Get predictions and probabilities
    predictions = model.predict(X.head(10))
    probabilities = model.predict_proba(X.head(10))
    
    print("\n   Sample Game Predictions:")
    print("   " + "-"*70)
    
    for i in range(min(5, len(X))):
        pred = "WIN" if predictions[i] == 1 else "LOSS"
        prob = probabilities[i][1] * 100  # Probability of winning
        
        print(f"   Game {i+1}:")
        print(f"      Your Rating: {X.iloc[i]['player_rating']:.0f}")
        print(f"      Opponent: {X.iloc[i]['opponent_rating']:.0f}")
        print(f"      Prediction: {pred} ({prob:.1f}% confidence)")
        print()


# ============================================================================
# MAIN PIPELINE
# ============================================================================

def run_pipeline():
    """Run complete ML pipeline"""
    
    try:
        # Load games
        games_data = load_games_from_db()
        if not games_data:
            return False
        
        # Engineer features
        X, y, features, df = engineer_features(games_data)
        
        # Train model
        model, X_train, X_test, y_train, y_test, features = train_xgboost_model(X, y, features)
        
        # SHAP explanations
        importance_df, explainer, shap_values = generate_shap_explanations(model, X_train, X_test, features)
        
        # Save model
        model_path, metadata_path = save_model(model, importance_df, features)
        
        # Sample predictions
        generate_sample_predictions(model, df, features)
        
        print("\n" + "="*70)
        print("✅ ML PIPELINE COMPLETE!")
        print("="*70)
        print(f"\n📊 Model ready for deployment:")
        print(f"   - Model file: {model_path}")
        print(f"   - Metadata: {metadata_path}")
        print(f"   - Features: {len(features)}")
        print(f"   - Training samples: {len(X_train)}")
        print(f"\n🚀 Next: Add prediction endpoint to API")
        print("="*70)
        
        return True
    
    except Exception as e:
        print(f"\n❌ Pipeline error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    run_pipeline()