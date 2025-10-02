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
            'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal',
            'bmi', 'smoking_status', 'alcohol_use'
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
                # Check if this looks like our text format (has Patient Age column)
                if 'Patient Age: 63' in df.columns or any('Patient Age:' in str(col) for col in df.columns):
                    # This is our text format, parse it properly
                    return self._parse_text_format(content)
                elif 'target' not in df.columns:
                    # Add target column if missing
                    df['target'] = np.random.randint(0, 2, len(df))
                return df
            except:
                # If CSV parsing fails, try to parse the text format
                return self._parse_text_format(content)
                
        except Exception as e:
            print(f"Error processing text file: {e}")
            return self._create_sample_data()
    
    def _parse_text_format(self, content: str) -> pd.DataFrame:
        """
        Parse the text format from heart.txt file.
        
        Args:
            content (str): File content
            
        Returns:
            pd.DataFrame: Parsed data
        """
        try:
            lines = content.strip().split('\n')
            data = []
            
            for line in lines:
                if line.strip() and 'Patient Age:' in line:
                    # Parse each line
                    record = self._parse_patient_line(line)
                    if record:
                        data.append(record)
            
            if not data:
                return self._create_sample_data()
            
            # Convert to DataFrame
            df = pd.DataFrame(data)
            
            # Ensure we have the right columns
            expected_columns = self.feature_names + ['target']
            for col in expected_columns:
                if col not in df.columns:
                    if col == 'target':
                        df[col] = np.random.randint(0, 2, len(df))
                    else:
                        df[col] = 0
            
            return df[expected_columns]
            
        except Exception as e:
            print(f"Error parsing text format: {e}")
            return self._create_sample_data()
    
    def _parse_patient_line(self, line: str) -> dict:
        """
        Parse a single patient line from the text file.
        
        Args:
            line (str): Patient data line
            
        Returns:
            dict: Parsed patient data
        """
        try:
            # Extract values using string parsing
            record = {}
            
            # Age
            age_match = line.split('Patient Age: ')[1].split(',')[0]
            record['age'] = int(age_match)
            
            # Gender (0=Female, 1=Male)
            gender_match = line.split('Gender: ')[1].split(',')[0]
            record['sex'] = 1 if gender_match.strip() == 'Male' else 0
            
            # Chest Pain Type
            cp_match = line.split('Chest Pain Type: ')[1].split(',')[0]
            record['cp'] = int(cp_match)
            
            # Resting BP
            bp_match = line.split('Resting BP: ')[1].split(' mmHg')[0]
            record['trestbps'] = int(bp_match)
            
            # Cholesterol
            chol_match = line.split('Cholesterol: ')[1].split(' mg/dl')[0]
            record['chol'] = int(chol_match)
            
            # Fasting Blood Sugar (0=No, 1=Yes)
            fbs_match = line.split('Fasting Blood Sugar: ')[1].split(',')[0]
            record['fbs'] = 1 if fbs_match.strip() == 'Yes' else 0
            
            # ECG Result
            ecg_match = line.split('ECG Result: ')[1].split(',')[0]
            record['restecg'] = int(ecg_match)
            
            # Max Heart Rate
            hr_match = line.split('Max Heart Rate: ')[1].split(',')[0]
            record['thalach'] = int(hr_match)
            
            # Exercise Angina (0=No, 1=Yes)
            exang_match = line.split('Exercise Angina: ')[1].split(',')[0]
            record['exang'] = 1 if exang_match.strip() == 'Yes' else 0
            
            # ST Depression
            st_match = line.split('ST Depression: ')[1].split(',')[0]
            record['oldpeak'] = float(st_match)
            
            # ST Slope
            slope_match = line.split('ST Slope: ')[1].split(',')[0]
            record['slope'] = int(slope_match)
            
            # Major Vessels
            vessels_match = line.split('Major Vessels: ')[1].split(',')[0]
            record['ca'] = int(vessels_match)
            
            # Thalassemia
            thal_match = line.split('Thalassemia: ')[1].split(',')[0]
            record['thal'] = int(thal_match)
            
            # BMI
            try:
                bmi_match = line.split('BMI: ')[1].split(',')[0]
                record['bmi'] = float(bmi_match)
            except:
                record['bmi'] = 25.0  # Default BMI
            
            # Smoking Status (0=Non-smoker, 1=Former smoker, 2=Current smoker)
            try:
                smoking_match = line.split('Smoking Status: ')[1].split(',')[0]
                if 'Non-smoker' in smoking_match:
                    record['smoking_status'] = 0
                elif 'Former smoker' in smoking_match:
                    record['smoking_status'] = 1
                elif 'Current smoker' in smoking_match:
                    record['smoking_status'] = 2
                else:
                    record['smoking_status'] = 0
            except:
                record['smoking_status'] = 0  # Default non-smoker
            
            # Alcohol Use (0=None, 1=Light, 2=Moderate, 3=Heavy)
            try:
                alcohol_match = line.split('Alcohol Use: ')[1].split(',')[0]
                if 'None' in alcohol_match:
                    record['alcohol_use'] = 0
                elif 'Light' in alcohol_match:
                    record['alcohol_use'] = 1
                elif 'Moderate' in alcohol_match:
                    record['alcohol_use'] = 2
                elif 'Heavy' in alcohol_match:
                    record['alcohol_use'] = 3
                else:
                    record['alcohol_use'] = 0
            except:
                record['alcohol_use'] = 0  # Default none
            
            # Disease Status (0=Negative, 1=Positive)
            disease_match = line.split('Disease Status: ')[1].split(',')[0]
            record['target'] = 1 if disease_match.strip() == 'Positive' else 0
            
            return record
            
        except Exception as e:
            print(f"Error parsing patient line: {e}")
            return None
    
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
            'bmi': np.random.uniform(18.5, 35.0, n_samples),
            'smoking_status': np.random.randint(0, 3, n_samples),
            'alcohol_use': np.random.randint(0, 4, n_samples),
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
