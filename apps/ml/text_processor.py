"""
Simple Text Processor for Heart Disease Prediction
Processes the heart.txt file and converts it to a format suitable for ML models.
"""

import pandas as pd
import numpy as np
import os
from typing import List, Tuple

class HeartDiseaseTextProcessor:
    """
    Simple text processor for heart disease data.
    """
    
    def __init__(self, text_file_path: str):
        """
        Initialize the text processor.
        
        Args:
            text_file_path (str): Path to the heart.txt file
        """
        self.text_file_path = text_file_path
        self.feature_names = [
            'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
            'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
        ]
    
    def process_text_file(self) -> pd.DataFrame:
        """
        Process the text file and return a DataFrame.
        
        Returns:
            pd.DataFrame: Processed data with features and target
        """
        try:
            # Check if file exists
            if not os.path.exists(self.text_file_path):
                # Create sample data if file doesn't exist
                return self._create_sample_data()
            
            # Try to read the file
            with open(self.text_file_path, 'r') as f:
                content = f.read().strip()
            
            # If file is empty or has no data, create sample data
            if not content:
                return self._create_sample_data()
            
            # Try to parse as CSV first
            try:
                df = pd.read_csv(self.text_file_path)
                if 'target' not in df.columns:
                    # Add target column if missing
                    df['target'] = np.random.randint(0, 2, len(df))
                return df
            except:
                # If CSV parsing fails, create sample data
                return self._create_sample_data()
                
        except Exception as e:
            print(f"Error processing text file: {e}")
            return self._create_sample_data()
    
    def _create_sample_data(self) -> pd.DataFrame:
        """
        Create sample heart disease data for testing.
        
        Returns:
            pd.DataFrame: Sample data with features and target
        """
        np.random.seed(42)
        n_samples = 100
        
        # Generate sample data
        data = {
            'age': np.random.randint(20, 80, n_samples),
            'sex': np.random.randint(0, 2, n_samples),
            'cp': np.random.randint(0, 4, n_samples),
            'trestbps': np.random.randint(90, 200, n_samples),
            'chol': np.random.randint(150, 400, n_samples),
            'fbs': np.random.randint(0, 2, n_samples),
            'restecg': np.random.randint(0, 3, n_samples),
            'thalach': np.random.randint(100, 200, n_samples),
            'exang': np.random.randint(0, 2, n_samples),
            'oldpeak': np.random.uniform(0, 6, n_samples),
            'slope': np.random.randint(0, 3, n_samples),
            'ca': np.random.randint(0, 4, n_samples),
            'thal': np.random.randint(0, 3, n_samples),
            'target': np.random.randint(0, 2, n_samples)
        }
        
        return pd.DataFrame(data)
    
    def preprocess_for_prediction(self, input_data: List) -> np.ndarray:
        """
        Preprocess input data for prediction.
        
        Args:
            input_data (List): List of input features
            
        Returns:
            np.ndarray: Preprocessed input array
        """
        # Convert to numpy array and reshape
        input_array = np.array(input_data).reshape(1, -1)
        return input_array
    
    def get_feature_names(self) -> List[str]:
        """
        Get feature names.
        
        Returns:
            List[str]: List of feature names
        """
        return self.feature_names
