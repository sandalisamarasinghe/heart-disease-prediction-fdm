"""
Model Integration for Django Application
Integrates the enhanced MLOps model with the Django heart disease prediction system.
"""

import joblib
import numpy as np
import pandas as pd
import os
from typing import List, Tuple, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HeartDiseasePredictor:
    """
    Production-ready heart disease predictor using the enhanced MLOps model.
    """
    
    def __init__(self, model_path: str = 'apps/ml/models/enhanced_mlops/'):
        """Initialize the predictor with trained models."""
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self.metadata = None
        self.feature_names = []
        self.is_loaded = False
        
        # Try to load the enhanced model
        self.load_models()
    
    def load_models(self):
        """Load the trained models and preprocessing objects."""
        try:
            model_file = os.path.join(self.model_path, 'best_model.pkl')
            scaler_file = os.path.join(self.model_path, 'scaler.pkl')
            metadata_file = os.path.join(self.model_path, 'metadata.pkl')
            
            if all(os.path.exists(f) for f in [model_file, scaler_file, metadata_file]):
                self.model = joblib.load(model_file)
                self.scaler = joblib.load(scaler_file)
                self.metadata = joblib.load(metadata_file)
                self.feature_names = self.metadata.get('feature_names', [])
                self.is_loaded = True
                
                logger.info(f"✅ Enhanced model loaded: {self.metadata['best_model_name']}")
                logger.info(f"Model accuracy: {self.metadata['performance_metrics'][self.metadata['best_model_name']]['accuracy']:.4f}")
                
            else:
                logger.warning("⚠️ Enhanced model not found, will use fallback prediction")
                self.is_loaded = False
                
        except Exception as e:
            logger.error(f"❌ Error loading enhanced model: {str(e)}")
            self.is_loaded = False
    
    def prepare_features(self, input_data: List[float]) -> np.ndarray:
        """
        Prepare input features for prediction.
        
        Args:
            input_data: List of 16 features [age, sex, cp, trestbps, chol, fbs, restecg, 
                       thalach, exang, oldpeak, slope, ca, thal, bmi, smoking_status, alcohol_use]
        
        Returns:
            Prepared feature array
        """
        try:
            # Convert to DataFrame for feature engineering
            base_features = [
                'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
                'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
            ]
            
            # Create DataFrame with base features
            df = pd.DataFrame([input_data[:13]], columns=base_features)
            
            # Add engineered features (same as in training)
            df = self._engineer_features(df)
            
            # Select only the features used in training
            if self.feature_names:
                # Ensure all required features are present
                for feature in self.feature_names:
                    if feature not in df.columns:
                        df[feature] = 0  # Default value for missing features
                
                df = df[self.feature_names]
            
            # Scale features
            if self.scaler:
                features_scaled = self.scaler.transform(df)
                return features_scaled
            else:
                return df.values
                
        except Exception as e:
            logger.error(f"Error preparing features: {str(e)}")
            # Return original features as fallback
            return np.array(input_data[:13]).reshape(1, -1)
    
    def _engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer features (same as in training)."""
        df_enhanced = df.copy()
        
        try:
            # Age-based risk categories
            df_enhanced['age_risk'] = pd.cut(df['age'], bins=[0, 45, 55, 65, 100], labels=[0, 1, 2, 3])
            df_enhanced['age_risk'] = df_enhanced['age_risk'].astype(int)
            
            # Cholesterol risk categories
            df_enhanced['chol_risk'] = pd.cut(df['chol'], bins=[0, 200, 240, 1000], labels=[0, 1, 2])
            df_enhanced['chol_risk'] = df_enhanced['chol_risk'].astype(int)
            
            # Blood pressure categories
            df_enhanced['bp_risk'] = pd.cut(df['trestbps'], bins=[0, 120, 140, 1000], labels=[0, 1, 2])
            df_enhanced['bp_risk'] = df_enhanced['bp_risk'].astype(int)
            
            # Heart rate efficiency
            df_enhanced['hr_efficiency'] = df['thalach'] / df['age']
            
            # Cardiovascular risk score
            risk_factors = []
            risk_factors.append((df['age'] > 50).astype(int))
            risk_factors.append(df['sex'])
            risk_factors.append((df['cp'] <= 1).astype(int))
            risk_factors.append((df['trestbps'] > 140).astype(int))
            risk_factors.append((df['chol'] > 240).astype(int))
            risk_factors.append(df['fbs'])
            risk_factors.append(df['exang'])
            risk_factors.append((df['oldpeak'] > 1).astype(int))
            risk_factors.append((df['ca'] > 0).astype(int))
            
            df_enhanced['cv_risk_score'] = sum(risk_factors)
            
            # Interaction features
            df_enhanced['age_chol'] = df['age'] * df['chol'] / 1000
            df_enhanced['age_bp'] = df['age'] * df['trestbps'] / 1000
            df_enhanced['sex_age'] = df['sex'] * df['age']
            
        except Exception as e:
            logger.error(f"Error in feature engineering: {str(e)}")
        
        return df_enhanced
    
    def predict(self, input_data: List[float]) -> Tuple[float, List[int]]:
        """
        Make prediction using the enhanced model or fallback.
        
        Args:
            input_data: List of input features
            
        Returns:
            Tuple of (confidence, [prediction])
        """
        try:
            if self.is_loaded and self.model is not None:
                # Use enhanced ML model
                features = self.prepare_features(input_data)
                
                # Get prediction and probability
                prediction = self.model.predict(features)[0]
                probabilities = self.model.predict_proba(features)[0]
                
                # Calculate confidence
                confidence = max(probabilities) * 100
                
                logger.info(f"Enhanced ML prediction: {prediction}, confidence: {confidence:.2f}%")
                return confidence, [int(prediction)]
            
            else:
                # Fallback to rule-based prediction
                return self._rule_based_prediction(input_data)
                
        except Exception as e:
            logger.error(f"Error in prediction: {str(e)}")
            # Ultimate fallback
            return self._rule_based_prediction(input_data)
    
    def _rule_based_prediction(self, input_data: List[float]) -> Tuple[float, List[int]]:
        """
        Enhanced rule-based prediction as fallback.
        """
        try:
            # Ensure we have enough features
            if len(input_data) < 13:
                return 75.0, [0]  # Default to healthy
            
            age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal = input_data[:13]
            
            # Enhanced rule-based scoring
            score = 0
            
            # Age factor (more granular)
            if age > 65:
                score += 3
            elif age > 55:
                score += 2
            elif age > 45:
                score += 1
            
            # Sex factor
            if sex == 1:  # Male
                score += 1
            
            # Chest pain (weighted by severity)
            if cp == 0:  # Typical angina
                score += 4
            elif cp == 1:  # Atypical angina
                score += 3
            elif cp == 2:  # Non-anginal pain
                score += 1
            
            # Blood pressure (more granular)
            if trestbps > 180:
                score += 3
            elif trestbps > 160:
                score += 2
            elif trestbps > 140:
                score += 1
            
            # Cholesterol (more granular)
            if chol > 300:
                score += 3
            elif chol > 240:
                score += 2
            elif chol > 200:
                score += 1
            
            # Other factors
            if fbs == 1:
                score += 1
            if exang == 1:
                score += 3  # Exercise angina is very significant
            if oldpeak > 2:
                score += 3
            elif oldpeak > 1:
                score += 2
            elif oldpeak > 0.5:
                score += 1
            
            # Major vessels (very significant)
            if ca > 2:
                score += 4
            elif ca > 1:
                score += 3
            elif ca > 0:
                score += 2
            
            # Thalassemia
            if thal == 1:  # Fixed defect
                score += 3
            elif thal == 2:  # Reversible defect
                score += 2
            
            # Additional features if available
            if len(input_data) >= 16:
                bmi, smoking_status, alcohol_use = input_data[13:16]
                
                # BMI factor
                if bmi >= 35:  # Severely obese
                    score += 3
                elif bmi >= 30:  # Obese
                    score += 2
                elif bmi >= 25:  # Overweight
                    score += 1
                elif bmi < 18.5:  # Underweight
                    score += 1
                
                # Smoking (very significant)
                if smoking_status == 2:  # Current smoker
                    score += 4
                elif smoking_status == 1:  # Former smoker
                    score += 2
                
                # Alcohol use
                if alcohol_use == 3:  # Heavy drinking
                    score += 2
                elif alcohol_use == 2:  # Moderate drinking
                    score += 1
            
            # Predict based on enhanced scoring
            if score >= 12:  # High risk threshold
                prediction = 1
                confidence = min(95.0, 75.0 + (score - 12) * 2)
            elif score >= 8:  # Medium-high risk
                prediction = 1
                confidence = min(85.0, 65.0 + (score - 8) * 2.5)
            elif score >= 5:  # Medium risk
                prediction = 0  # Still healthy but monitor
                confidence = min(80.0, 60.0 + (8 - score) * 2)
            else:  # Low risk
                prediction = 0
                confidence = min(95.0, 75.0 + (5 - score) * 3)
            
            logger.info(f"Rule-based prediction: score={score}, prediction={prediction}, confidence={confidence:.2f}%")
            return confidence, [prediction]
            
        except Exception as e:
            logger.error(f"Error in rule-based prediction: {str(e)}")
            return 75.0, [0]  # Safe default
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        if self.is_loaded and self.metadata:
            return {
                'model_name': self.metadata['best_model_name'],
                'accuracy': self.metadata['performance_metrics'][self.metadata['best_model_name']]['accuracy'],
                'training_date': self.metadata['training_date'],
                'features_count': len(self.feature_names),
                'status': 'Enhanced ML Model'
            }
        else:
            return {
                'model_name': 'Rule-based System',
                'accuracy': 0.75,  # Estimated
                'training_date': 'N/A',
                'features_count': 16,
                'status': 'Fallback Model'
            }


# Global predictor instance
_predictor = None

def get_predictor() -> HeartDiseasePredictor:
    """Get or create the global predictor instance."""
    global _predictor
    if _predictor is None:
        _predictor = HeartDiseasePredictor()
    return _predictor

def predict_heart_disease(input_data: List[float]) -> Tuple[float, List[int]]:
    """
    Main prediction function for Django integration.
    
    Args:
        input_data: List of 16 features
        
    Returns:
        Tuple of (confidence, [prediction])
    """
    predictor = get_predictor()
    return predictor.predict(input_data)

def get_model_status() -> Dict[str, Any]:
    """Get current model status for admin interface."""
    predictor = get_predictor()
    return predictor.get_model_info()
