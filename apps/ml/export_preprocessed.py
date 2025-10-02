"""
Utility to export preprocessed dataset from data/heart.txt to CSV.

Outputs:
 - data/preprocessed_heart.csv              (raw parsed features + target)
 - data/preprocessed_heart_capped.csv       (features capped using saved IQR bounds, if available)
"""

import os
import sys
from pathlib import Path
import pandas as pd
import joblib

# Ensure project root is on path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from apps.ml.text_processor import HeartDiseaseTextProcessor


def main():
    input_path = PROJECT_ROOT / 'data' / 'heart.txt'
    output_path = PROJECT_ROOT / 'data' / 'preprocessed_heart.csv'
    capped_output_path = PROJECT_ROOT / 'data' / 'preprocessed_heart_capped.csv'
    bounds_path = PROJECT_ROOT / 'apps' / 'ml' / 'models' / 'outlier_bounds.pkl'

    processor = HeartDiseaseTextProcessor(str(input_path))
    df = processor.process_text_file()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Saved: {output_path} (rows={len(df)}, cols={len(df.columns)})")

    # Attempt to export a capped version using saved outlier bounds from training
    try:
        if bounds_path.exists():
            saved_bounds = joblib.load(bounds_path)
            lower = pd.Series(saved_bounds.get('lower'))
            upper = pd.Series(saved_bounds.get('upper'))
            feature_cols = processor.get_feature_names()
            # Align and cap only feature columns; keep target unchanged
            df_features = df[feature_cols].copy()
            lower_aligned = lower.reindex(df_features.columns)
            upper_aligned = upper.reindex(df_features.columns)
            df_features_capped = df_features.clip(lower=lower_aligned, upper=upper_aligned, axis=1)
            df_capped = pd.concat([df_features_capped, df[['target']]], axis=1)
            df_capped.to_csv(capped_output_path, index=False)
            print(f"Saved (capped): {capped_output_path} (rows={len(df_capped)}, cols={len(df_capped.columns)})")
        else:
            print(f"Warning: {bounds_path} not found. Skipping capped export. Train a model first to generate outlier bounds.")
    except Exception as e:
        print(f"Warning: Failed to export capped CSV due to: {e}")


if __name__ == '__main__':
    main()


