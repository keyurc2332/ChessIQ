# ml_models/feature_engineering.py

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder

def engineer_features(df_games, df_moves):
    """
    Engineer advanced features from games and moves data
    """
    
    print("🔧 Engineering features...")
    
    # Basic features (already have)
    X = df_games[[
        'player_rating_before', 
        'opponent_rating', 
        'accuracy', 
        'avg_centipawn_loss',
        'time_control'
    ]].copy()
    
    # Feature 1: Rating difference
    X['rating_difference'] = X['player_rating_before'] - df_games['opponent_rating']
    
    # Feature 2: Time control encoding
    le = LabelEncoder()
    X['time_control_encoded'] = le.fit_transform(X['time_control'].fillna('unknown'))
    
    # Feature 3: Opening ECO encoding
    le_opening = LabelEncoder()
    X['opening_encoded'] = le_opening.fit_transform(df_games['opening_eco'].fillna('unknown'))
    
    # Feature 4: Player color encoding
    X['player_color_encoded'] = (df_games['player_color'] == 'white').astype(int)
    
    # Feature 5: Accuracy-CPL interaction
    X['accuracy_cpl_interaction'] = X['accuracy'] * X['avg_centipawn_loss']
    
    # Feature 6: Win expectancy (based on rating difference)
    # Using simplified Elo calculation
    X['win_expectancy'] = 1 / (1 + 10**(-X['rating_difference']/400))
    
    # Drop original time_control column
    X = X.drop('time_control', axis=1)
    
    # Fill NaN values
    X = X.fillna(X.mean())
    
    # Normalize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)
    
    print(f"✅ Features engineered: {X_scaled_df.shape[1]} features")
    print(f"   Features: {list(X_scaled_df.columns)}")
    
    return X_scaled_df, X.columns, scaler

def get_target(df_games):
    """Get target variable (win = 1, loss/draw = 0)"""
    y = (df_games['result'] == 'win').astype(int)
    print(f"✅ Target variable created")
    print(f"   Class distribution: {y.value_counts().to_dict()}")
    return y