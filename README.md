# ♟️ ChessIQ

### AI-Powered Chess Analytics & Improvement Platform

![Chess](https://img.shields.io/badge/Chess-Analytics-blue?style=for-the-badge)
![ML](https://img.shields.io/badge/Machine%20Learning-72.49%25-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-yellow?style=for-the-badge)

---

## 🎯 Overview

ChessIQ is a **production-ready machine learning platform** that analyzes chess performance, identifies strengths/weaknesses, and **predicts game outcomes with 72.49% accuracy** using only pre-game features.

Built with **real data** (4,635 games, 328,258 moves), this project demonstrates the full data science lifecycle: from data collection and exploratory analysis to feature engineering, model training, and interactive deployment.

---

## 🌟 Key Features

### 📊 **Comprehensive Analytics**
- **4,635 real games analyzed** from Chess.com (2021-2026)
- **328,258 moves evaluated** with Stockfish engine (depth=15)
- Win rate, accuracy, and rating progression tracking
- Opening performance breakdown (best: 60.26%, worst: 39.19%)
- Time control effectiveness analysis

### 🤖 **AI Predictions**
- **Pre-game outcome predictor** - 72.49% accuracy
- **Multiple ML models**: XGBoost, Random Forest, Gradient Boosting, Ensemble
- **SHAP feature importance** - Understand what drives predictions
- **Model consensus scoring** - Confidence levels for each prediction
- **Historical comparison** - Similar game recommendations

### 💡 **Smart Recommendations**
- Personalized improvement tips based on data
- Opening strategy recommendations (play D31 more!)
- Opponent strength analysis & strategy
- Time control performance insights
- Data-driven action plans

### 📈 **Interactive Dashboard**
- 8 beautiful, responsive pages
- Real-time visualizations with Plotly
- Mobile-friendly design
- Smooth animations & transitions

---

## 📈 Project Highlights

### 📊 Dataset
```
Total Games:          4,635
Time Span:            5 years (2021-2026)
Total Moves:          328,258
Win Rate:             49.1% (2,276 wins)
Average Accuracy:     91.93%
Rating Improvement:   +826 points (+138%)
```

### 🤖 ML Model Performance
```
Best Model:           Voting Ensemble
Accuracy:             72.49%
AUC-ROC:              0.8265
Cross-Validation:     5-fold (74-76% range)
Data Leakage:         ✅ FIXED (pre-game features only)
```

### 🎯 Top Insights

| Metric | Finding |
|--------|---------|
| **Strongest Predictor** | Rating Difference (59.63% importance) |
| **vs Weaker Players** | 88.4% win rate (50-100 rating gap) |
| **Best Opening** | D31: 60.26% win rate |
| **Worst Opening** | A04: 39.19% win rate |
| **Consistency** | Only 1.8% variance across time controls |
| **Rating Growth** | 597 → 1,423 (+138% in 5 years) |

---

## 🏗️ Technology Stack

### **Backend & ML**
- **Python 3.10+** - Core language
- **FastAPI** - REST API framework
- **PostgreSQL** - Database (Railway)
- **SQLAlchemy** - ORM

### **Data Science & ML**
- **scikit-learn** - ML algorithms & evaluation
- **XGBoost** - Gradient boosting models
- **TensorFlow/Keras** - Neural networks
- **Pandas & NumPy** - Data manipulation
- **Jupyter** - Exploratory analysis

### **Chess Analysis**
- **Stockfish** - Chess engine (depth=15 analysis)
- **python-chess** - Chess logic

### **Frontend**
- **Streamlit** - Interactive dashboard
- **Plotly** - Advanced visualizations
- **HTML/CSS** - Custom styling

### **Deployment**
- **Streamlit Cloud** - Frontend hosting
- **Railway** - Database hosting
- **GitHub** - Version control

---

## 📁 Project Structure

```
ChessIQ/
│
├── backend/
│   ├── main.py                          # FastAPI server
│   ├── database.py                      # SQLAlchemy models & DB connection
│   ├── requirements.txt                 # Backend dependencies
│   │
│   ├── ml_models/
│   │   ├── feature_engineering.py       # Feature creation & preprocessing
│   │   ├── model_training.py            # Training pipeline
│   │   ├── model_comparison.py          # Model evaluation
│   │   └── __init__.py
│   │
│   ├── notebooks/
│   │   ├── 01_exploratory_analysis.ipynb        # EDA (4,635 games)
│   │   ├── 04_ml_training.ipynb                 # With data leakage (reference)
│   │   └── 05_ml_training_no_leakage.ipynb      # Fixed version ✅
│   │
│   ├── results/
│   │   ├── models/
│   │   │   ├── best_model_gb.pkl
│   │   │   ├── scaler.pkl
│   │   │   └── feature_names.pkl
│   │   ├── visualizations/                      # Charts & graphs
│   │   └── reports/
│   │       ├── eda_report.md
│   │       └── PROJECT_SUMMARY.txt
│   │
│   └── venv/                            # Virtual environment
│
├── frontend/
│   ├── app.py                           # Streamlit dashboard (main file)
│   ├── requirements.txt                 # Frontend dependencies
│   └── .streamlit/
│       └── config.toml
│
├── README.md                            # This file
├── .gitignore
└── LICENSE
```

---

## 🚀 Quick Start

### **Local Development**

#### 1. Clone the Repository
```bash
git clone https://github.com/keyurc2332/ChessIQ.git
cd ChessIQ
```

#### 2. Frontend Setup
```bash
cd frontend

# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\activate          # Windows
source venv/bin/activate         # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Opens at: **http://localhost:8501**

#### 3. Backend Setup (Optional - for API)
```bash
cd backend

python -m venv venv
.\venv\Scripts\activate

pip install -r requirements.txt

python main.py
```

---

## 📊 Dashboard Pages

### **1. 📊 Dashboard**
- Overall performance KPIs (4,635 games, 49.1% win rate, 91.93% accuracy)
- Game results distribution pie chart
- Accuracy histogram

### **2. 🎯 Opening Analysis**
- Top 10 openings by win rate
- D31: 60.26% (strongest)
- A04: 39.19% (weakest)
- Recommendations: Play D31 more, study A04

### **3. ⚔️ Opponent Strength**
- Win rate by rating difference
- 88.4% vs weaker (-50 to -100)
- 6.6% vs much stronger (-100+)
- Strategic recommendations

### **4. ⏱️ Time Control**
- Performance across Blitz, Rapid, Classical, Long
- Win rate consistency (47.7%-49.5%, only 1.8% variance)
- Centipawn loss by format

### **5. 📈 5-Year Progress**
- Rating progression: 597 → 1,423 (+826)
- Win rate trend: 44.5% → 57.1% (upward)
- Time series analysis & insights

### **6. 🔮 Win Predictor**
- **AI-powered game outcome prediction**
- Input: Your rating, opponent rating, time control, color
- Output: Win probability (72.49% accuracy)
- Feature contribution analysis
- Similar games from history

### **7. 💡 AI Tips**
- **Play More**: D31 (60.26%), D20 (54.26%), A40 (53.99%)
- **Study More**: A04 (39.19%), B20 (40.77%)
- **Seek**: Opponents 50-100 points weaker (88.4% win)
- **Action Plan**: Weekly, monthly, quarterly goals

### **8. 🤖 ML Insights**
- Feature importance visualization (SHAP)
- Model details (accuracy, AUC-ROC, training data)
- Key findings & explanations

---

## 🔍 Key Findings & Insights

### ✅ Strengths
- ⭐ Excellent consistency: 91.93% average accuracy
- ⭐ Dominates weaker opponents: 88.4% win rate
- ⭐ Solid opening repertoire: D31, D20, A40
- ⭐ Steady improvement: +826 rating over 5 years
- ⭐ Time control flexibility: Equally good in all formats

### ⚠️ Weaknesses
- 🔴 Weak in A04 (39.19%) and B20 (40.77%) openings
- 🔴 Lower win rate vs equal/stronger opponents
- 🔴 Loses by being outplayed, not just blunders
- 🔴 Needs work on positional play & middlegame

### 💡 Data-Driven Recommendations

**This Week:**
- Play D31 openings (60% win rate)
- Seek opponents 50-100 points weaker
- Avoid A04

**This Month:**
- Study B20 opening theory
- Play Classical games for analysis
- Focus on endgame technique

**This Quarter:**
- Master D31 & D20 completely
- Challenge opponents ±20 rating
- Target 1,250+ rating

---

## 🔧 Data Leakage: How I Fixed It

### ❌ Original Problem
Initial model used **post-game metrics**:
- Accuracy % (unknown before game)
- Centipawn Loss (unknown before game)
- Accuracy-CPL interaction (unknown before game)

Result: **Inflated 78.21% accuracy** (unrealistic!)

### ✅ Solution
Refactored to use **only pre-game features**:
1. Player rating before game
2. Opponent rating
3. Rating difference
4. Historical win rate (cumulative)
5. Average opponent rating history
6. Recent win streak (last 10 games)
7. Time control
8. Player color

Result: **Honest 72.49% accuracy** (production-ready!)

### 📊 Impact
```
Before (Leakage):      78.21% accuracy ❌
After (Leakage Fixed): 72.49% accuracy ✅

Drop: 5.72% (expected and healthy!)
Status: Production-ready ✅
```

This demonstrates understanding of **ML best practices** and **data integrity**.

---

## 🎓 Technical Approach

### **1. Exploratory Data Analysis (EDA)**
- Win rate breakdown by opening, rating, time control
- Correlation analysis (accuracy vs CPL: -0.763)
- Time series analysis (24 windows, 200 games each)
- Statistical distributions

### **2. Feature Engineering**
- Created 8 pre-game features
- Handled missing values (forward fill)
- Standardized scaling (StandardScaler)
- Feature interaction removal (no leakage)

### **3. Model Training**
**5 Models Trained:**
- XGBoost (72.17% accuracy)
- Random Forest (72.17% accuracy)
- Gradient Boosting (72.06% accuracy)
- Voting Ensemble (72.49% accuracy) ⭐
- Stacking Ensemble (71.84% accuracy)

### **4. Model Evaluation**
- 80/20 train-test split
- 5-fold cross-validation
- McNemar's statistical test
- Confusion matrix & ROC curves
- Hyperparameter tuning (GridSearchCV)

### **5. Deployment**
- Saved models as pickle files
- FastAPI REST endpoints
- Streamlit interactive dashboard
- Real-time predictions

---

## 📚 Learning Outcomes

This project demonstrates:

✅ **Full ML Lifecycle**
- Data collection & preprocessing
- Exploratory analysis
- Feature engineering
- Model training & evaluation
- Deployment & monitoring

✅ **Data Science Best Practices**
- Data leakage detection & fixing
- Cross-validation & statistical testing
- Hyperparameter tuning
- Model explainability (SHAP)

✅ **Software Engineering**
- Clean code & documentation
- Version control (Git)
- API design (FastAPI)
- Frontend development (Streamlit)

✅ **Domain Expertise**
- Chess understanding & analysis
- Strategic thinking
- Real-world problem solving

✅ **Product Thinking**
- User-centric design
- Actionable insights
- Recommendation systems

---

## 🎯 Use Cases

### **For Chess Players**
- Identify your best/worst openings
- Understand your rating dynamics
- Get personalized improvement tips
- Predict game difficulty before playing

### **For Data Scientists**
- Reference for full ML pipeline
- Example of fixing data leakage
- Ensemble methods demonstration
- Streamlit dashboard patterns

### **For Recruiters & Employers**
- Portfolio of real-world skills
- Production-quality code
- Statistical rigor & best practices
- Full project ownership

---

## 🚀 Future Enhancements

- [ ] Expand to 50k+ multi-player games
- [ ] Use move sequences (LSTM) instead of aggregated features
- [ ] Add move-by-move analysis
- [ ] Integrate live Chess.com API
- [ ] Build recommendation engine for training
- [ ] Deploy to AWS/GCP for scalability
- [ ] Mobile app version
- [ ] Multiplayer comparison (play vs others)

---

## 📄 Resume Impact

**One-liner:**
```
ChessIQ: AI-powered chess analytics platform with 72.49% ML prediction 
accuracy, analyzing 4,635 real games and 328K moves.
```

**Full Bullet:**
```
ChessIQ: AI Chess Analytics Platform
• Analyzed 4,635 real Chess.com games with Stockfish engine (depth=15),
  generating 328,258 move evaluations & engineered 8 pre-game features
• Built ML ensemble achieving 72.49% win prediction accuracy; identified
  rating difference as strongest predictor (59.63% feature importance)
• Demonstrated statistical rigor: 5-fold cross-validation, McNemar's testing,
  hyperparameter tuning; fixed critical data leakage issue
• Developed interactive Streamlit dashboard with 8 analytical pages, Plotly
  visualizations, and personalized improvement recommendations
• Technologies: Python, TensorFlow, scikit-learn, XGBoost, FastAPI,
  PostgreSQL, Stockfish, Jupyter, Streamlit
```

---

## 🔗 Links

- **GitHub**: https://github.com/keyurc2332/ChessIQ
- **LinkedIn**: https://www.linkedin.com/in/keyur-chauhan-/

---

## 📞 Questions?

This project is designed to be **understandable and reproducible**. Check the notebooks for detailed analysis or reach out!

---

## 📝 License

MIT License - Free to use for learning and research.

---

## 🙏 Acknowledgments

- **Chess.com** - Game data API
- **Stockfish** - Chess engine
- **scikit-learn** - ML algorithms

---

**Built with ❤️ for Data Science & Chess** | Last Updated: June 2026
