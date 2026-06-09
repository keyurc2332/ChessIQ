# ml_models/model_comparison.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def compare_models(results_dict):
    """Compare all model results"""
    
    print("\n" + "="*60)
    print("MODEL COMPARISON RESULTS")
    print("="*60)
    
    # Create comparison dataframe
    comparison_df = pd.DataFrame(results_dict).T
    comparison_df = comparison_df.sort_values('Accuracy', ascending=False)
    
    print("\n", comparison_df.to_string())
    
    # Visualization
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle('Model Performance Comparison', fontsize=16, fontweight='bold')
    
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1', 'AUC-ROC']
    
    for idx, metric in enumerate(metrics):
        ax = axes[idx // 3, idx % 3]
        values = comparison_df[metric]
        colors = ['green' if v == values.max() else 'skyblue' for v in values]
        
        ax.barh(values.index, values.values, color=colors, edgecolor='black', linewidth=1.5)
        ax.set_xlabel(metric, fontweight='bold')
        ax.set_title(f'{metric} Comparison', fontweight='bold')
        ax.set_xlim([0, 1])
        ax.grid(alpha=0.3, axis='x')
        
        # Add value labels
        for i, v in enumerate(values.values):
            ax.text(v + 0.01, i, f'{v:.3f}', va='center', fontweight='bold')
    
    # Remove extra subplot
    axes[1, 2].remove()
    
    plt.tight_layout()
    plt.savefig('results/visualizations/model_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"\n✅ Comparison chart saved to results/visualizations/model_comparison.png")
    
    # Get best model
    best_model = comparison_df.index[0]
    best_accuracy = comparison_df.iloc[0]['Accuracy']
    
    print(f"\n🏆 BEST MODEL: {best_model} ({best_accuracy:.4f} accuracy)")
    
    return comparison_df

def save_comparison(results_dict, path='results/reports/'):
    """Save comparison to CSV"""
    df = pd.DataFrame(results_dict).T
    df.to_csv(f'{path}model_comparison.csv')
    print(f"✅ Comparison saved to {path}model_comparison.csv")