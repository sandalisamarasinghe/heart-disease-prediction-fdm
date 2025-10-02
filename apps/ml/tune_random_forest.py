"""
Hyperparameter sweep for RandomForest with existing preprocessing:
 - Parses data via HeartDiseaseTextProcessor
 - Train/test split (stratified)
 - IQR capping on train; apply to test
 - StandardScaler on capped features
 - GridSearchCV on RandomForestClassifier

Prints best params, CV score, and test accuracy.
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Project path setup
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from apps.ml.heart_disease_model import HeartDiseaseModel


def main():
    model = HeartDiseaseModel(text_file_path=str(PROJECT_ROOT / 'data' / 'heart.txt'))

    # Load raw features and target
    X, y = model.load_and_preprocess_data()

    # Hold-out split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # IQR capping using training bounds
    lower, upper = model._compute_outlier_bounds(X_train)
    X_train_cap = model._apply_outlier_capping(X_train, lower, upper)
    X_test_cap = model._apply_outlier_capping(X_test, lower, upper)

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_cap)
    X_test_scaled = scaler.transform(X_test_cap)

    # RF and grid
    rf = RandomForestClassifier(
        random_state=42, class_weight='balanced_subsample', n_jobs=-1
    )
    param_grid = {
        'n_estimators': [200, 400],
        'max_depth': [8, 12, None],
        'min_samples_leaf': [1, 3],
        'max_features': ['sqrt']
    }
    cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    gs = GridSearchCV(
        rf, param_grid, scoring='accuracy', cv=cv, n_jobs=-1, verbose=1
    )
    gs.fit(X_train_scaled, y_train)

    # Evaluate on hold-out
    best_rf = gs.best_estimator_
    y_pred = best_rf.predict(X_test_scaled)
    test_acc = accuracy_score(y_test, y_pred)

    print('\nBEST PARAMS:', gs.best_params_)
    print('CV BEST SCORE (accuracy):', round(gs.best_score_, 4))
    print('TEST ACCURACY:', round(test_acc, 4))


if __name__ == '__main__':
    main()





