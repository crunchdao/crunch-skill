# Submission Optimization Guide

Complete workflow for uploading, analyzing, and optimizing ML submissions in CrunchDAO competitions.

## Overview

The submission optimization cycle follows these phases:
1. **Initial Submission** - Get baseline performance  
2. **Performance Analysis** - Deep dive into metrics and leaderboard position
3. **Strategic Improvement** - Targeted feature engineering and model architecture changes
4. **Iterative Refinement** - Systematic testing and validation
5. **Portfolio Management** - Multi-submission strategy and timing

## Phase 1: Initial Submission

### Download and Explore Data
```bash
# Download competition data
crunch download

# Examine data structure
ls -la data/
head -10 data/train.csv
head -10 data/test.csv

# Check data quality
python3 -c "
import pandas as pd
train = pd.read_csv('data/train.csv')
print(f'Train shape: {train.shape}')
print(f'Columns: {list(train.columns)}')
print(f'Null values: {train.isnull().sum().sum()}')
print(f'Target distribution: {train.iloc[:,-1].describe()}')
"
```

### Create Baseline Model
Start with a simple, robust model to establish baseline performance:

```python
# baseline_model.py
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
import numpy as np

def create_baseline():
    # Load data
    train = pd.read_csv('data/train.csv')
    X = train.iloc[:, :-1]  # Features
    y = train.iloc[:, -1]   # Target
    
    # Handle missing values
    X = X.fillna(X.median())
    
    # Simple model
    model = RandomForestRegressor(
        n_estimators=100, 
        random_state=42,
        n_jobs=-1
    )
    
    # Cross-validation to estimate performance
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='neg_mean_squared_error')
    print(f"CV RMSE: {np.sqrt(-cv_scores.mean()):.4f} (+/- {np.sqrt(-cv_scores.std() * 2):.4f})")
    
    # Fit on full training set
    model.fit(X, y)
    
    # Generate predictions
    test = pd.read_csv('data/test.csv')
    test_features = test.fillna(test.median())
    predictions = model.predict(test_features)
    
    # Save predictions
    submission = pd.DataFrame({'prediction': predictions})
    submission.to_csv('submission.csv', index=False)
    
    return model

if __name__ == "__main__":
    model = create_baseline()
```

### Submit Baseline
```bash
# Test locally
crunch test

# Submit if test passes
crunch push -m "Baseline RandomForest model"
```

## Phase 2: Performance Analysis

### Dashboard Analysis
1. Visit [CrunchDAO Dashboard](https://crunchdao.com) 
2. Navigate to your competition
3. Check leaderboard position and score
4. Compare against percentiles (25th, 50th, 75th, 95th)

### Detailed Performance Review
```python
# analyze_performance.py
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

def analyze_submission_performance():
    """Analyze model performance and identify improvement areas"""
    
    # Load data and predictions
    train = pd.read_csv('data/train.csv')
    X_train = train.iloc[:, :-1]
    y_train = train.iloc[:, -1]
    
    # Recreate model for analysis
    from sklearn.ensemble import RandomForestRegressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    X_train_filled = X_train.fillna(X_train.median())
    model.fit(X_train_filled, y_train)
    
    # Analyze feature importance
    feature_importance = pd.DataFrame({
        'feature': X_train.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("Top 10 Features:")
    print(feature_importance.head(10))
    
    # Analyze residuals
    train_pred = model.predict(X_train_filled)
    residuals = y_train - train_pred
    
    print(f"\nTraining RMSE: {np.sqrt(mean_squared_error(y_train, train_pred)):.4f}")
    print(f"Residual mean: {residuals.mean():.4f}")
    print(f"Residual std: {residuals.std():.4f}")
    
    # Plot residuals
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.scatter(train_pred, residuals, alpha=0.5)
    plt.xlabel('Predictions')
    plt.ylabel('Residuals')
    plt.title('Residual Plot')
    plt.axhline(y=0, color='r', linestyle='--')
    
    plt.subplot(1, 2, 2)
    plt.hist(residuals, bins=50, alpha=0.7)
    plt.xlabel('Residuals')
    plt.ylabel('Frequency')
    plt.title('Residual Distribution')
    
    plt.tight_layout()
    plt.savefig('performance_analysis.png')
    print("\nSaved analysis plots to performance_analysis.png")
    
    return feature_importance, residuals

if __name__ == "__main__":
    feature_importance, residuals = analyze_submission_performance()
```

## Phase 3: Strategic Improvement

### Feature Engineering
Based on performance analysis, implement targeted feature improvements:

```python
# feature_engineering.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, PolynomialFeatures

def engineer_features(df):
    """Advanced feature engineering based on analysis"""
    df = df.copy()
    
    # 1. Handle missing values more intelligently
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            df[f'{col}_is_missing'] = df[col].isnull().astype(int)
            df[col] = df[col].fillna(df[col].median())
    
    # 2. Create interaction features for top features
    # (Based on feature importance analysis)
    top_features = ['feature1', 'feature2', 'feature3']  # Update based on analysis
    for i, feat1 in enumerate(top_features):
        for feat2 in top_features[i+1:]:
            if feat1 in df.columns and feat2 in df.columns:
                df[f'{feat1}_{feat2}_interaction'] = df[feat1] * df[feat2]
                df[f'{feat1}_{feat2}_ratio'] = df[feat1] / (df[feat2] + 1e-8)
    
    # 3. Statistical features
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df['feature_mean'] = df[numeric_cols].mean(axis=1)
    df['feature_std'] = df[numeric_cols].std(axis=1)
    df['feature_skew'] = df[numeric_cols].skew(axis=1)
    
    # 4. Binning continuous variables
    for col in numeric_cols[:5]:  # Top 5 numeric features
        df[f'{col}_binned'] = pd.qcut(df[col], q=5, labels=False, duplicates='drop')
    
    return df

def create_improved_model():
    """Improved model with feature engineering"""
    
    # Load and engineer features
    train = pd.read_csv('data/train.csv')
    X_train = engineer_features(train.iloc[:, :-1])
    y_train = train.iloc[:, -1]
    
    test = pd.read_csv('data/test.csv')
    X_test = engineer_features(test)
    
    # Advanced model ensemble
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.linear_model import Ridge
    from sklearn.model_selection import cross_val_score
    
    models = {
        'rf': RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42),
        'gbm': GradientBoostingRegressor(n_estimators=200, learning_rate=0.1, random_state=42),
        'ridge': Ridge(alpha=1.0)
    }
    
    # Train models and get predictions
    predictions = {}
    for name, model in models.items():
        # Cross-validation
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
        print(f"{name} CV RMSE: {np.sqrt(-cv_scores.mean()):.4f}")
        
        # Fit and predict
        model.fit(X_train, y_train)
        predictions[name] = model.predict(X_test)
    
    # Ensemble predictions (weighted average)
    weights = {'rf': 0.4, 'gbm': 0.4, 'ridge': 0.2}
    ensemble_pred = np.average([predictions[name] for name in weights.keys()], 
                              weights=list(weights.values()), axis=0)
    
    # Save submission
    submission = pd.DataFrame({'prediction': ensemble_pred})
    submission.to_csv('improved_submission.csv', index=False)
    
    return models, ensemble_pred

if __name__ == "__main__":
    models, predictions = create_improved_model()
```

### Hyperparameter Optimization
```python
# hyperparameter_tuning.py
from sklearn.model_selection import RandomizedSearchCV, cross_val_score
from sklearn.ensemble import RandomForestRegressor
import numpy as np

def optimize_hyperparameters():
    """Systematic hyperparameter optimization"""
    
    # Load engineered data
    train = pd.read_csv('data/train.csv')
    X_train = engineer_features(train.iloc[:, :-1])  # From previous step
    y_train = train.iloc[:, -1]
    
    # Define parameter space
    param_distributions = {
        'n_estimators': [100, 200, 300, 500],
        'max_depth': [5, 10, 15, 20, None],
        'min_samples_split': [2, 5, 10, 20],
        'min_samples_leaf': [1, 2, 5, 10],
        'max_features': ['auto', 'sqrt', 'log2', 0.5, 0.7]
    }
    
    # Random search
    rf = RandomForestRegressor(random_state=42, n_jobs=-1)
    random_search = RandomizedSearchCV(
        rf, param_distributions, 
        n_iter=50, cv=3, 
        scoring='neg_mean_squared_error',
        random_state=42, n_jobs=-1
    )
    
    random_search.fit(X_train, y_train)
    
    print(f"Best parameters: {random_search.best_params_}")
    print(f"Best CV score: {np.sqrt(-random_search.best_score_):.4f}")
    
    return random_search.best_estimator_

if __name__ == "__main__":
    best_model = optimize_hyperparameters()
```

## Phase 4: Iterative Refinement

### Systematic Testing Framework
```bash
# Create testing framework
mkdir experiments
cd experiments

# Track experiment results
echo "experiment,cv_score,leaderboard_score,notes" > experiment_log.csv
```

```python
# experiment_framework.py
import pandas as pd
import numpy as np
from datetime import datetime
import json

class ExperimentTracker:
    def __init__(self, log_file="experiment_log.csv"):
        self.log_file = log_file
        
    def log_experiment(self, name, cv_score, leaderboard_score=None, notes=""):
        """Log experiment results"""
        experiment = {
            'timestamp': datetime.now().isoformat(),
            'experiment': name,
            'cv_score': cv_score,
            'leaderboard_score': leaderboard_score,
            'notes': notes
        }
        
        df = pd.DataFrame([experiment])
        if os.path.exists(self.log_file):
            df.to_csv(self.log_file, mode='a', header=False, index=False)
        else:
            df.to_csv(self.log_file, index=False)
            
    def get_best_experiments(self, top_n=5):
        """Get best performing experiments"""
        df = pd.read_csv(self.log_file)
        return df.nsmallest(top_n, 'cv_score')

# Usage
tracker = ExperimentTracker()

# Run experiment
cv_score = run_cross_validation()  # Your CV function
tracker.log_experiment("ensemble_v2", cv_score, notes="Added interaction features")
```

### Validation Strategy
```python
# robust_validation.py
from sklearn.model_selection import TimeSeriesSplit, KFold, cross_val_score
import numpy as np

def robust_validation(model, X, y, is_time_series=False):
    """Robust cross-validation strategy"""
    
    if is_time_series:
        cv = TimeSeriesSplit(n_splits=5)
    else:
        cv = KFold(n_splits=5, shuffle=True, random_state=42)
    
    # Multiple scoring metrics
    scoring = ['neg_mean_squared_error', 'neg_mean_absolute_error', 'r2']
    
    results = {}
    for score in scoring:
        scores = cross_val_score(model, X, y, cv=cv, scoring=score)
        results[score] = {
            'mean': scores.mean(),
            'std': scores.std(),
            'scores': scores
        }
    
    # Print results
    print("Validation Results:")
    print("-" * 40)
    for metric, stats in results.items():
        print(f"{metric}: {stats['mean']:.4f} (+/- {stats['std'] * 2:.4f})")
    
    return results

# Safety checks before submission
def pre_submission_checks():
    """Safety checks before submitting"""
    
    # 1. Check file format
    submission = pd.read_csv('submission.csv')
    print(f"Submission shape: {submission.shape}")
    print(f"Columns: {list(submission.columns)}")
    
    # 2. Check for missing values
    if submission.isnull().sum().sum() > 0:
        print("⚠️  WARNING: Submission contains missing values!")
        
    # 3. Check prediction range
    pred_min, pred_max = submission['prediction'].min(), submission['prediction'].max()
    print(f"Prediction range: [{pred_min:.4f}, {pred_max:.4f}]")
    
    # 4. Check for infinite values
    if np.isinf(submission['prediction']).any():
        print("⚠️  WARNING: Submission contains infinite values!")
        
    # 5. Statistical checks
    pred_mean = submission['prediction'].mean()
    pred_std = submission['prediction'].std()
    print(f"Prediction stats - Mean: {pred_mean:.4f}, Std: {pred_std:.4f}")
    
    return True  # All checks passed

if __name__ == "__main__":
    # Example usage
    from sklearn.ensemble import RandomForestRegressor
    
    # Load data
    train = pd.read_csv('data/train.csv')
    X, y = train.iloc[:, :-1], train.iloc[:, -1]
    X = X.fillna(X.median())
    
    # Model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    # Validate
    results = robust_validation(model, X, y)
    
    # Safety checks
    pre_submission_checks()
```

## Phase 5: Portfolio Management

### Multi-Submission Strategy
```python
# portfolio_strategy.py
import pandas as pd
from datetime import datetime, timedelta

class SubmissionPortfolio:
    def __init__(self):
        self.submissions = []
        
    def add_submission(self, name, cv_score, strategy, timestamp=None):
        if timestamp is None:
            timestamp = datetime.now()
            
        self.submissions.append({
            'name': name,
            'cv_score': cv_score,
            'strategy': strategy,
            'timestamp': timestamp,
            'leaderboard_score': None
        })
    
    def update_leaderboard_score(self, name, score):
        for sub in self.submissions:
            if sub['name'] == name:
                sub['leaderboard_score'] = score
                break
    
    def get_portfolio_summary(self):
        df = pd.DataFrame(self.submissions)
        return df.sort_values('cv_score')
    
    def should_submit(self, cv_score, threshold=0.001):
        """Decide if new model is worth submitting"""
        if not self.submissions:
            return True
            
        best_cv = min(sub['cv_score'] for sub in self.submissions)
        improvement = best_cv - cv_score
        
        return improvement > threshold

# Usage
portfolio = SubmissionPortfolio()
portfolio.add_submission("baseline", 0.1234, "RandomForest baseline")
portfolio.add_submission("engineered", 0.1189, "Feature engineering + ensemble")

print(portfolio.get_portfolio_summary())
```

### Timing Strategy
```python
# timing_strategy.py
from datetime import datetime, timedelta
import pandas as pd

def calculate_submission_timing(competition_end, current_time=None):
    """Strategic timing for submissions"""
    
    if current_time is None:
        current_time = datetime.now()
    
    time_remaining = competition_end - current_time
    days_remaining = time_remaining.days
    
    print(f"Days remaining: {days_remaining}")
    
    # Submission strategy based on time remaining
    if days_remaining > 7:
        strategy = "EXPLORATION"
        advice = "Focus on experimentation and feature engineering"
    elif days_remaining > 3:
        strategy = "OPTIMIZATION"  
        advice = "Fine-tune best models, ensemble strategies"
    elif days_remaining > 1:
        strategy = "REFINEMENT"
        advice = "Small improvements to best model, safety checks"
    else:
        strategy = "FINAL"
        advice = "Submit only if significantly better, focus on reliability"
    
    print(f"Strategy: {strategy}")
    print(f"Advice: {advice}")
    
    return strategy

# Example usage
competition_end = datetime(2026, 3, 15, 23, 59, 59)
strategy = calculate_submission_timing(competition_end)
```

## Best Practices

### Code Quality
```python
# Always include these in your models

def create_reproducible_model():
    """Template for reproducible model creation"""
    
    # 1. Set random seeds
    import random
    import numpy as np
    random.seed(42)
    np.random.seed(42)
    
    # 2. Version control your data processing
    def preprocess_data(df, version="v1"):
        if version == "v1":
            return df.fillna(df.median())
        elif version == "v2":
            # More sophisticated preprocessing
            pass
    
    # 3. Save model configuration
    config = {
        'model_type': 'RandomForest',
        'parameters': {'n_estimators': 100, 'random_state': 42},
        'preprocessing_version': 'v1',
        'feature_engineering': ['interactions', 'binning'],
        'timestamp': datetime.now().isoformat()
    }
    
    with open('model_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    return model, config
```

### Performance Monitoring
```bash
# Create monitoring script
echo '#!/bin/bash
# monitor_competition.sh

echo "Competition Status: $(date)"
echo "============================="

# Check leaderboard position
crunch status

# Check submission history  
ls -la submissions/

# Resource usage
echo "Disk usage: $(du -sh .)"
echo "Memory usage: $(free -h)"

' > monitor_competition.sh

chmod +x monitor_competition.sh
```

### Emergency Procedures
```bash
# emergency_rollback.sh
#!/bin/bash

echo "🚨 Emergency Rollback Procedure"
echo "==============================="

# 1. Backup current work
timestamp=$(date +%Y%m%d_%H%M%S)
mkdir -p backups
cp -r . backups/emergency_backup_$timestamp/

# 2. Revert to last known good submission
if [ -f "submissions/last_good_submission.csv" ]; then
    cp submissions/last_good_submission.csv submission.csv
    echo "✅ Reverted to last good submission"
else
    echo "❌ No backup submission found!"
fi

# 3. Quick test
crunch test

if [ $? -eq 0 ]; then
    echo "✅ Test passed, ready to submit"
    read -p "Submit now? (y/n): " -n 1 -r
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        crunch push -m "Emergency rollback submission"
    fi
else
    echo "❌ Test failed, manual intervention required"
fi
```

## Common Pitfalls

1. **Overfitting to CV:** Always validate improvements on holdout set
2. **Data leakage:** Ensure no future information in features
3. **Submission format:** Double-check file format before submitting
4. **Time management:** Don't leave submissions to the last minute
5. **Model complexity:** Balance complexity with generalization
6. **Feature scaling:** Ensure consistent scaling between train/test
7. **Missing value handling:** Consistent strategy across all data

## Competition-Specific Optimizations

### For Time Series Competitions
- Use TimeSeriesSplit for cross-validation
- Respect temporal order in features
- Consider lag features and rolling windows

### For Image Competitions  
- Data augmentation strategies
- Transfer learning from pre-trained models
- Ensemble different architectures

### For Tabular Competitions
- Feature engineering and selection
- Ensemble diverse model types
- Handle categorical variables appropriately

### For NLP Competitions
- Text preprocessing and tokenization
- Word embeddings and transformer models
- Sequence modeling strategies

---

Remember: Consistent, methodical improvement beats sporadic breakthroughs. Track everything, validate rigorously, and submit strategically.