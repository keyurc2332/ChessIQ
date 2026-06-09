
# ChessIQ - Exploratory Data Analysis Report

## Dataset Overview
- Total Games Analyzed: 4,635
- Date Range: 2021-06-02 to 2026-06-08
- Average Player Rating: 965
- Average Opponent Rating: 965

## Performance Metrics
- Win Rate: 49.1% (2,276 wins)
- Loss Rate: 45.7% (2,120 losses)
- Draw Rate: 5.2% (239 draws)
- Average Accuracy: 91.93%
- Average CPL: 141.48

## Key Insights

### 1. Rating Difference is CRITICAL
- vs Weaker (50-100): 88.4% win rate [BEST]
- vs Equal (+0 to +50): 65.7% win rate
- vs Equal (-50 to 0): 32.6% win rate
- vs Stronger (-100 to -50): 6.6% win rate

### 2. Opening Mastery
- Best: D31 (60.3% win rate)
- Strong: D20 (54.3%), A40 (54.0%)
- Weak: A04 (39.2%), B20 (40.8%)

### 3. Time Control Consistency
- Blitz (60s): 49.5% win rate, 91.95% accuracy
- Rapid (180s): 48.9% win rate, 91.75% accuracy
- Classical (300s): 47.7% win rate, 92.52% accuracy
→ HIGHLY CONSISTENT across formats!

### 4. Feature Correlations
- Accuracy-CPL: -0.763 (strong inverse)
- Player-Opponent Rating: 0.755 (balanced matchups)
- Player Rating-Accuracy: -0.009 (no correlation)

## ML Features Prepared
[OK] Player Rating
[OK] Opponent Rating  
[OK] Rating Difference (KEY FEATURE)
[OK] Accuracy
[OK] Centipawn Loss
[OK] Time Control
[OK] Opening ECO
[OK] Player Color
[OK] Feature Interactions

## Next Steps
1. Complete move analysis (570,000+ moves)
2. Engineer advanced features
3. Train 5 ML models
4. Compare and select best model
5. Create SHAP explanability
6. Generate predictions

## Data Quality
- No missing critical data
- Balanced class distribution (49% win rate)
- Sufficient samples for training
- Good feature diversity

---
Report Generated: 2026-06-09
Status: Ready for ML Phase
