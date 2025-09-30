"""
Enhanced Heart Disease Prediction Model
Uses unstructured text data and advanced machine learning algorithms.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os
from typing import Tuple, Dict, Any, List
import logging

from .text_processor import HeartDiseaseTextProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HeartDiseaseModel:
    """
    Advanced Heart Disease Prediction Model using unstructured text data.
    """
    
    def __init__(self, text_file_path: str, model_save_path: str = 'apps/ml/models/'):
        """
        Initialize the heart disease prediction model.
        
        Args:
            text_file_path (str): Path to the heart.txt file
            model_save_path (str): Directory to save trained models
        """
        self.text_file_path = text_file_path
        self.model_save_path = model_save_path
        self.text_processor = HeartDiseaseTextProcessor(text_file_path)
        
        # Initialize models
        self.models = {}
        self.scaler = StandardScaler()
        # Outlier bounds learned on training data (persisted with model)
        self.outlier_lower_bounds = None
        self.outlier_upper_bounds = None
        self.best_model = None
        self.best_accuracy = 0.0
        
        # Create model directory if it doesn't exist
        os.makedirs(model_save_path, exist_ok=True)
        
        # Improved model configurations for better accuracy
        self.model_configs = {
            'random_forest': {
                'model': RandomForestClassifier(
                    random_state=42,
                    n_estimators=200,
                    max_depth=15,
                    min_samples_split=5,
                    class_weight='balanced_subsample'
                ),
                'params': {}
            },
            'logistic_regression': {
                'model': LogisticRegression(random_state=42, max_iter=1000, C=1.0, class_weight='balanced'),
                'params': {}
            },
            'gradient_boosting': {
                'model': GradientBoostingClassifier(random_state=42, n_estimators=100, max_depth=6),
                'params': {}
            }
        }
    
    def load_and_preprocess_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Load and preprocess the text data.
        
        Returns:
            Tuple[pd.DataFrame, pd.Series]: Features (X) and target (y)
        """
        try:
            # Process the text file
            df = self.text_processor.process_text_file()
            
            # Sample data for faster training (use 5000 records max for better accuracy)
            if len(df) > 5000:
                df = df.sample(n=5000, random_state=42)
                logger.info(f"Sampled {len(df)} records for training")
            
            # Separate features and target
            X = df.drop('target', axis=1)
            y = df['target']
            
            logger.info(f"Loaded {len(df)} records with {len(X.columns)} features")
            logger.info(f"Target distribution: {y.value_counts().to_dict()}")
            
            return X, y
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def train_models(self, test_size: float = 0.2, random_state: int = 42) -> Dict[str, float]:
        """
        Train all models and find the best performing one.
        
        Args:
            test_size (float): Proportion of data for testing
            random_state (int): Random seed for reproducibility
            
        Returns:
            Dict[str, float]: Dictionary of model accuracies
        """
        try:
            # Load and preprocess data
            X, y = self.load_and_preprocess_data()
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=random_state, stratify=y
            )
            
            # Compute IQR-based outlier bounds on training data and persist
            self.outlier_lower_bounds, self.outlier_upper_bounds = self._compute_outlier_bounds(X_train)
            
            # Apply outlier capping using training bounds to both train and test
            X_train_capped = self._apply_outlier_capping(X_train, self.outlier_lower_bounds, self.outlier_upper_bounds)
            X_test_capped = self._apply_outlier_capping(X_test, self.outlier_lower_bounds, self.outlier_upper_bounds)
            
            # Scale features on capped data
            X_train_scaled = self.scaler.fit_transform(X_train_capped)
            X_test_scaled = self.scaler.transform(X_test_capped)
            
            accuracies = {}
            
            # Train each model (simplified for speed)
            for name, config in self.model_configs.items():
                logger.info(f"Training {name}...")
                
                try:
                    # Simple training without grid search for speed
                    model = config['model']
                    model.fit(X_train_scaled, y_train)
                    self.models[name] = model
                    
                    # Evaluate
                    y_pred = model.predict(X_test_scaled)
                    accuracy = accuracy_score(y_test, y_pred)
                    accuracies[name] = accuracy
                    
                    logger.info(f"{name} - Accuracy: {accuracy:.4f}")
                    
                    # Update best model if this one is better
                    if accuracy > self.best_accuracy:
                        self.best_accuracy = accuracy
                        self.best_model = model
                        
                except Exception as e:
                    logger.error(f"Error training {name}: {str(e)}")
                    accuracies[name] = 0.0
            
            # Create ensemble model
            self._create_ensemble_model(X_train_scaled, y_train)
            
            # Save the best model
            self._save_best_model()
            
            return accuracies
            
        except Exception as e:
            logger.error(f"Error in training: {str(e)}")
            raise

    def _compute_outlier_bounds(self, X_train: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
        """
        Compute IQR-based lower/upper bounds for outlier capping on numeric features.
        """
        try:
            Q1 = X_train.quantile(0.25)
            Q3 = X_train.quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            return lower, upper
        except Exception as e:
            logger.error(f"Error computing outlier bounds: {str(e)}")
            # Fallback: no capping
            zeros = X_train.iloc[0:1].drop(X_train.iloc[0:1].index).reindex(columns=X_train.columns).fillna(0)
            return zeros.squeeze(), zeros.squeeze()

    def _apply_outlier_capping(self, X: pd.DataFrame, lower: pd.Series, upper: pd.Series) -> pd.DataFrame:
        """
        Apply clipping to the provided DataFrame using precomputed bounds.
        """
        try:
            # Align indexes to avoid broadcasting issues
            lower_aligned = lower.reindex(X.columns)
            upper_aligned = upper.reindex(X.columns)
            return X.clip(lower=lower_aligned, upper=upper_aligned, axis=1)
        except Exception as e:
            logger.error(f"Error applying outlier capping: {str(e)}")
            return X
    
    def _create_ensemble_model(self, X_train: np.ndarray, y_train: np.ndarray):
        """
        Create an ensemble model combining the best performing models.
        
        Args:
            X_train (np.ndarray): Training features
            y_train (np.ndarray): Training targets
        """
        try:
            # Get models with accuracy > 0.8
            good_models = []
            for name, model in self.models.items():
                if hasattr(model, 'score'):
                    score = model.score(X_train, y_train)
                    if score > 0.8:
                        good_models.append((name, model))
            
            if len(good_models) > 1:
                # Create voting classifier
                estimators = [(name, model) for name, model in good_models]
                self.ensemble_model = VotingClassifier(
                    estimators=estimators,
                    voting='soft'
                )
                
                # Train ensemble
                self.ensemble_model.fit(X_train, y_train)
                self.models['ensemble'] = self.ensemble_model
                
                logger.info(f"Created ensemble model with {len(good_models)} base models")
            
        except Exception as e:
            logger.error(f"Error creating ensemble: {str(e)}")
    
    def _save_best_model(self):
        """
        Save the best performing model to disk.
        """
        try:
            if self.best_model is not None:
                model_path = os.path.join(self.model_save_path, 'best_heart_disease_model.pkl')
                scaler_path = os.path.join(self.model_save_path, 'scaler.pkl')
                bounds_path = os.path.join(self.model_save_path, 'outlier_bounds.pkl')
                
                joblib.dump(self.best_model, model_path)
                joblib.dump(self.scaler, scaler_path)
                # Save outlier bounds for use at inference
                joblib.dump({
                    'lower': self.outlier_lower_bounds,
                    'upper': self.outlier_upper_bounds
                }, bounds_path)
                
                logger.info(f"Best model saved to {model_path}")
                logger.info(f"Scaler saved to {scaler_path}")
                logger.info(f"Outlier bounds saved to {bounds_path}")
                
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
    
    def load_saved_model(self) -> bool:
        """
        Load a previously saved model.
        
        Returns:
            bool: True if model loaded successfully, False otherwise
        """
        try:
            model_path = os.path.join(self.model_save_path, 'best_heart_disease_model.pkl')
            scaler_path = os.path.join(self.model_save_path, 'scaler.pkl')
            bounds_path = os.path.join(self.model_save_path, 'outlier_bounds.pkl')
            
            if os.path.exists(model_path) and os.path.exists(scaler_path):
                self.best_model = joblib.load(model_path)
                self.scaler = joblib.load(scaler_path)
                if os.path.exists(bounds_path):
                    saved_bounds = joblib.load(bounds_path)
                    self.outlier_lower_bounds = saved_bounds.get('lower')
                    self.outlier_upper_bounds = saved_bounds.get('upper')
                logger.info("Loaded saved model successfully")
                return True
            else:
                logger.warning("No saved model found")
                return False
                
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return False
    
    def predict(self, input_data: List) -> Tuple[int, float]:
        """
        Make a prediction using the best model.
        
        Args:
            input_data (List): List of input features
            
        Returns:
            Tuple[int, float]: Prediction (0 or 1) and confidence score
        """
        try:
            if self.best_model is None:
                raise ValueError("No trained model available. Please train the model first.")
            
            # Preprocess input
            input_array = self.text_processor.preprocess_for_prediction(input_data)
            
            # Convert to DataFrame for capping using stored bounds
            feature_names = self.text_processor.get_feature_names()
            input_df = pd.DataFrame(input_array, columns=feature_names)
            if self.outlier_lower_bounds is not None and self.outlier_upper_bounds is not None:
                input_df = self._apply_outlier_capping(input_df, self.outlier_lower_bounds, self.outlier_upper_bounds)
            
            # Scale input
            input_scaled = self.scaler.transform(input_df.values)
            
            # Make prediction
            prediction = self.best_model.predict(input_scaled)[0]
            
            # Get confidence score (probability)
            if hasattr(self.best_model, 'predict_proba'):
                confidence = self.best_model.predict_proba(input_scaled)[0]
                confidence_score = max(confidence)
            else:
                confidence_score = 0.8  # Default confidence for models without predict_proba
            
            return int(prediction), confidence_score
            
        except Exception as e:
            logger.error(f"Error in prediction: {str(e)}")
            raise
    
    def get_model_performance(self) -> Dict[str, Any]:
        """
        Get detailed performance metrics for all models.
        
        Returns:
            Dict[str, Any]: Performance metrics
        """
        try:
            X, y = self.load_and_preprocess_data()
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            X_test_scaled = self.scaler.transform(X_test)
            
            performance = {}
            
            for name, model in self.models.items():
                try:
                    y_pred = model.predict(X_test_scaled)
                    accuracy = accuracy_score(y_test, y_pred)
                    
                    # Classification report
                    report = classification_report(y_test, y_pred, output_dict=True)
                    
                    # Confusion matrix
                    cm = confusion_matrix(y_test, y_pred)
                    
                    performance[name] = {
                        'accuracy': accuracy,
                        'precision': report['weighted avg']['precision'],
                        'recall': report['weighted avg']['recall'],
                        'f1_score': report['weighted avg']['f1-score'],
                        'confusion_matrix': cm.tolist()
                    }
                    
                except Exception as e:
                    logger.error(f"Error evaluating {name}: {str(e)}")
                    performance[name] = {'error': str(e)}
            
            return performance
            
        except Exception as e:
            logger.error(f"Error getting performance: {str(e)}")
            return {}
    
    def get_feature_importance(self) -> Dict[str, float]:
        """
        Get feature importance from the best model.
        
        Returns:
            Dict[str, float]: Feature importance scores
        """
        try:
            if self.best_model is None:
                return {}
            
            feature_names = self.text_processor.get_feature_names()
            
            if hasattr(self.best_model, 'feature_importances_'):
                importance = self.best_model.feature_importances_
            elif hasattr(self.best_model, 'coef_'):
                importance = np.abs(self.best_model.coef_[0])
            else:
                return {}
            
            return dict(zip(feature_names, importance))
            
        except Exception as e:
            logger.error(f"Error getting feature importance: {str(e)}")
            return {}
