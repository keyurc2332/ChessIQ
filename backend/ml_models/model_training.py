# ml_models/model_training.py

import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import warnings
warnings.filterwarnings('ignore')

class ModelTrainer:
    def __init__(self, X, y):
        self.X = X
        self.y = y
        self.models = {}
        self.results = {}
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"✅ Data split: {len(self.X_train)} train, {len(self.X_test)} test")
    
    def train_xgboost(self):
        """Train XGBoost model"""
        print("\n🚀 Training XGBoost...")
        
        model = XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            eval_metric='logloss'
        )
        
        model.fit(self.X_train, self.y_train)
        self.models['XGBoost'] = model
        
        self._evaluate(model, 'XGBoost')
    
    def train_random_forest(self):
        """Train Random Forest model"""
        print("\n🌲 Training Random Forest...")
        
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(self.X_train, self.y_train)
        self.models['Random Forest'] = model
        
        self._evaluate(model, 'Random Forest')
    
    def train_gradient_boosting(self):
        """Train Gradient Boosting model"""
        print("\n📈 Training Gradient Boosting...")
        
        model = GradientBoostingClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
        
        model.fit(self.X_train, self.y_train)
        self.models['Gradient Boosting'] = model
        
        self._evaluate(model, 'Gradient Boosting')
    
    def train_logistic_regression(self):
        """Train Logistic Regression baseline"""
        print("\n📊 Training Logistic Regression...")
        
        model = LogisticRegression(
            max_iter=1000,
            random_state=42
        )
        
        model.fit(self.X_train, self.y_train)
        self.models['Logistic Regression'] = model
        
        self._evaluate(model, 'Logistic Regression')
    
    def _evaluate(self, model, name):
        """Evaluate model performance"""
        y_pred = model.predict(self.X_test)
        y_pred_proba = model.predict_proba(self.X_test)[:, 1]
        
        results = {
            'Accuracy': accuracy_score(self.y_test, y_pred),
            'Precision': precision_score(self.y_test, y_pred),
            'Recall': recall_score(self.y_test, y_pred),
            'F1': f1_score(self.y_test, y_pred),
            'AUC-ROC': roc_auc_score(self.y_test, y_pred_proba)
        }
        
        self.results[name] = results
        
        print(f"   Accuracy: {results['Accuracy']:.4f}")
        print(f"   Precision: {results['Precision']:.4f}")
        print(f"   Recall: {results['Recall']:.4f}")
        print(f"   F1: {results['F1']:.4f}")
        print(f"   AUC-ROC: {results['AUC-ROC']:.4f}")
    
    def train_all(self):
        """Train all models"""
        self.train_xgboost()
        self.train_random_forest()
        self.train_gradient_boosting()
        self.train_logistic_regression()
        
        return self.models, self.results
    
    def save_models(self, path='results/models/'):
        """Save trained models"""
        for name, model in self.models.items():
            filename = f"{path}{name.replace(' ', '_').lower()}.pkl"
            with open(filename, 'wb') as f:
                pickle.dump(model, f)
            print(f"✅ Saved {name} to {filename}")