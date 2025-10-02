"""
Enhanced Heart Disease Prediction Model with Advanced ML Techniques
Implements feature engineering, hyperparameter optimization, and ensemble methods for maximum accuracy.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, RandomizedSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler, MinMaxScaler, PolynomialFeatures, RobustScaler
from sklearn.ensemble import (
    GradientBoostingClassifier, RandomForestClassifier, VotingClassifier, 
    ExtraTreesClassifier, AdaBoostClassifier, BaggingClassifier
)
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix, 
    roc_auc_score, precision_recall_curve, roc_curve, f1_score
)
from sklearn.feature_selection import SelectKBest, f_classif, RFE
import joblib
import os
from typing import Tuple, Dict, Any, List
import logging
import warnings
warnings.filterwarnings('ignore')

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("XGBoost not available. Install with: pip install xgboost")

try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False
    print("LightGBM not available. Install with: pip install lightgbm")

try:
    from .text_processor import HeartDiseaseTextProcessor
except ImportError:
    from text_processor import HeartDiseaseTextProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedHeartDiseaseModel:
    """
    Enhanced Heart Disease Prediction Model with advanced ML techniques.
    """
    
    def __init__(self, text_file_path: str, model_save_path: str = 'apps/ml/models/'):
        """
        Initialize the enhanced heart disease prediction model.
        
        Args:
            text_file_path (str): Path to the heart.txt file
            model_save_path (str): Directory to save trained models
        """
        self.text_file_path = text_file_path
        self.model_save_path = model_save_path
        self.text_processor = HeartDiseaseTextProcessor(text_file_path)
        
        # Initialize models and preprocessors
        self.models = {}
        self.scaler = RobustScaler()  # More robust to outliers
        self.poly_features = PolynomialFeatures(degree=2, include_bias=False, interaction_only=True)
        self.feature_selector = SelectKBest(f_classif, k='all')
        
        # Model performance tracking
        self.best_model = None
        self.best_accuracy = 0.0
        self.best_model_name = ""
        self.cv_scores = {}
        
        # Create model directory if it doesn't exist
        os.makedirs(model_save_path, exist_ok=True)
        
        # Enhanced model configurations with hyperparameter ranges
        self.model_configs = self._get_model_configs()
    
    def _get_model_configs(self) -> Dict:
        """Get enhanced model configurations with hyperparameter ranges."""
        configs = {
            'random_forest': {
                'model': RandomForestClassifier(random_state=42, n_jobs=-1),
                'params': {
                    'n_estimators': [100, 200, 300, 500],
                    'max_depth': [10, 15, 20, None],
                    'min_samples_split': [2, 5, 10],
                    'min_samples_leaf': [1, 2, 4],
                    'class_weight': ['balanced', 'balanced_subsample']
                }
            },
            'gradient_boosting': {
                'model': GradientBoostingClassifier(random_state=42),
                'params': {
                    'n_estimators': [100, 200, 300],
                    'learning_rate': [0.05, 0.1, 0.15, 0.2],
                    'max_depth': [3, 5, 7, 9],
                    'subsample': [0.8, 0.9, 1.0]
                }
            },
            'logistic_regression': {
                'model': LogisticRegression(random_state=42, max_iter=2000),
                'params': {
                    'C': [0.01, 0.1, 1, 10, 100],
                    'penalty': ['l1', 'l2', 'elasticnet'],
                    'solver': ['liblinear', 'saga'],
                    'class_weight': ['balanced', None]
                }
            },
            'svm': {
                'model': SVC(random_state=42, probability=True),
                'params': {
                    'C': [0.1, 1, 10, 100],
                    'kernel': ['rbf', 'poly', 'sigmoid'],
                    'gamma': ['scale', 'auto', 0.001, 0.01, 0.1],
                    'class_weight': ['balanced', None]
                }
            },
            'neural_network': {
                'model': MLPClassifier(random_state=42, max_iter=1000),
                'params': {
                    'hidden_layer_sizes': [(50,), (100,), (50, 50), (100, 50), (100, 100)],
                    'activation': ['relu', 'tanh', 'logistic'],
                    'alpha': [0.0001, 0.001, 0.01],
                    'learning_rate': ['constant', 'adaptive']
                }
            },
            'extra_trees': {
                'model': ExtraTreesClassifier(random_state=42, n_jobs=-1),
                'params': {
                    'n_estimators': [100, 200, 300],
                    'max_depth': [10, 15, 20, None],
                    'min_samples_split': [2, 5, 10],
                    'class_weight': ['balanced', 'balanced_subsample']
                }
            },
            'knn': {
                'model': KNeighborsClassifier(n_jobs=-1),
                'params': {
                    'n_neighbors': [3, 5, 7, 9, 11],
                    'weights': ['uniform', 'distance'],
                    'metric': ['euclidean', 'manhattan', 'minkowski']
                }
            }
        }
        
        # Add XGBoost if available
        if XGBOOST_AVAILABLE:
            configs['xgboost'] = {
                'model': xgb.XGBClassifier(random_state=42, eval_metric='logloss'),
                'params': {
                    'n_estimators': [100, 200, 300],
                    'learning_rate': [0.05, 0.1, 0.2],
                    'max_depth': [3, 5, 7],
                    'subsample': [0.8, 0.9, 1.0],
                    'colsample_bytree': [0.8, 0.9, 1.0]
                }
            }
        
        # Add LightGBM if available
        if LIGHTGBM_AVAILABLE:
            configs['lightgbm'] = {
                'model': lgb.LGBMClassifier(random_state=42, verbose=-1),
                'params': {
                    'n_estimators': [100, 200, 300],
                    'learning_rate': [0.05, 0.1, 0.2],
                    'max_depth': [3, 5, 7],
                    'num_leaves': [31, 50, 100],
                    'subsample': [0.8, 0.9, 1.0]
                }
            }
        
        return configs
    
    def load_and_preprocess_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Load and preprocess the text data with enhanced feature engineering.
        
        Returns:
            Tuple[pd.DataFrame, pd.Series]: Features (X) and target (y)
        """
        try:
            # Process the text file
            df = self.text_processor.process_text_file()
            
            # Use more data for better training (up to 10000 records)
            if len(df) > 10000:
                df = df.sample(n=10000, random_state=42)
                logger.info(f"Sampled {len(df)} records for training")
            
            # Separate features and target
            X = df.drop('target', axis=1)
            y = df['target']
            
            # Feature Engineering
            X = self._engineer_features(X)
            
            logger.info(f"Loaded {len(df)} records with {len(X.columns)} features after engineering")
            logger.info(f"Target distribution: {y.value_counts().to_dict()}")
            
            return X, y
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def _engineer_features(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Engineer additional features to improve model performance.
        
        Args:
            X (pd.DataFrame): Input features
            
        Returns:
            pd.DataFrame: Enhanced features
        """
        try:
            X_enhanced = X.copy()
            
            # Age-based features
            X_enhanced['age_group'] = pd.cut(X['age'], bins=[0, 30, 45, 60, 100], labels=[0, 1, 2, 3])
            X_enhanced['age_group'] = X_enhanced['age_group'].astype(int)
            
            # BMI categories (if BMI exists)
            if 'bmi' in X.columns:
                X_enhanced['bmi_category'] = pd.cut(X['bmi'], 
                                                   bins=[0, 18.5, 25, 30, 100], 
                                                   labels=[0, 1, 2, 3])
                X_enhanced['bmi_category'] = X_enhanced['bmi_category'].astype(int)
            
            # Cholesterol risk levels
            if 'chol' in X.columns:
                X_enhanced['chol_risk'] = pd.cut(X['chol'], 
                                               bins=[0, 200, 240, 1000], 
                                               labels=[0, 1, 2])
                X_enhanced['chol_risk'] = X_enhanced['chol_risk'].astype(int)
            
            # Blood pressure categories
            if 'trestbps' in X.columns:
                X_enhanced['bp_category'] = pd.cut(X['trestbps'], 
                                                 bins=[0, 120, 140, 1000], 
                                                 labels=[0, 1, 2])
                X_enhanced['bp_category'] = X_enhanced['bp_category'].astype(int)
            
            # Heart rate zones
            if 'thalach' in X.columns:
                X_enhanced['hr_zone'] = pd.cut(X['thalach'], 
                                             bins=[0, 100, 150, 200, 1000], 
                                             labels=[0, 1, 2, 3])
                X_enhanced['hr_zone'] = X_enhanced['hr_zone'].astype(int)
            
            # Risk interaction features
            if all(col in X.columns for col in ['age', 'chol', 'trestbps']):
                X_enhanced['age_chol_interaction'] = X['age'] * X['chol'] / 1000
                X_enhanced['age_bp_interaction'] = X['age'] * X['trestbps'] / 1000
            
            if all(col in X.columns for col in ['smoking_status', 'age']):
                X_enhanced['smoking_age_risk'] = X['smoking_status'] * (X['age'] / 50)
            
            # Cardiovascular risk score (simplified)
            risk_factors = []
            if 'age' in X.columns:
                risk_factors.append((X['age'] > 45).astype(int))
            if 'sex' in X.columns:
                risk_factors.append(X['sex'])  # Male = 1
            if 'smoking_status' in X.columns:
                risk_factors.append((X['smoking_status'] > 0).astype(int))
            if 'chol' in X.columns:
                risk_factors.append((X['chol'] > 240).astype(int))
            if 'trestbps' in X.columns:
                risk_factors.append((X['trestbps'] > 140).astype(int))
            
            if risk_factors:
                X_enhanced['cv_risk_score'] = sum(risk_factors)
            
            logger.info(f"Feature engineering complete. Added {len(X_enhanced.columns) - len(X.columns)} new features")
            
            return X_enhanced
            
        except Exception as e:
            logger.error(f"Error in feature engineering: {str(e)}")
            return X
    
    def train_models_with_optimization(self, test_size: float = 0.2, random_state: int = 42, 
                                     use_grid_search: bool = True, cv_folds: int = 5) -> Dict[str, float]:
        """
        Train all models with hyperparameter optimization.
        
        Args:
            test_size (float): Proportion of data for testing
            random_state (int): Random seed for reproducibility
            use_grid_search (bool): Whether to use grid search for hyperparameter tuning
            cv_folds (int): Number of cross-validation folds
            
        Returns:
            Dict[str, float]: Dictionary of model accuracies
        """
        try:
            # Load and preprocess data
            X, y = self.load_and_preprocess_data()
            
            # Split data with stratification
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=random_state, stratify=y
            )
            
            # Handle missing values
            X_train = X_train.fillna(X_train.median())
            X_test = X_test.fillna(X_train.median())  # Use training median for test
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Feature selection (optional)
            # X_train_scaled = self.feature_selector.fit_transform(X_train_scaled, y_train)
            # X_test_scaled = self.feature_selector.transform(X_test_scaled)
            
            accuracies = {}
            cv_scores = {}
            
            # Cross-validation setup
            cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=random_state)
            
            # Train each model
            for name, config in self.model_configs.items():
                logger.info(f"Training {name}...")
                
                try:
                    model = config['model']
                    
                    if use_grid_search and config['params']:
                        # Use RandomizedSearchCV for faster optimization
                        search = RandomizedSearchCV(
                            model, 
                            config['params'], 
                            cv=cv, 
                            scoring='accuracy',
                            n_iter=20,  # Reduced for speed
                            random_state=random_state,
                            n_jobs=-1,
                            verbose=0
                        )
                        search.fit(X_train_scaled, y_train)
                        best_model = search.best_estimator_
                        logger.info(f"{name} best params: {search.best_params_}")
                    else:
                        # Simple training without optimization
                        best_model = model
                        best_model.fit(X_train_scaled, y_train)
                    
                    self.models[name] = best_model
                    
                    # Cross-validation score
                    cv_score = cross_val_score(best_model, X_train_scaled, y_train, cv=cv, scoring='accuracy')
                    cv_scores[name] = cv_score.mean()
                    
                    # Test accuracy
                    y_pred = best_model.predict(X_test_scaled)
                    accuracy = accuracy_score(y_test, y_pred)
                    accuracies[name] = accuracy
                    
                    logger.info(f"{name} - CV Score: {cv_score.mean():.4f} (+/- {cv_score.std() * 2:.4f})")
                    logger.info(f"{name} - Test Accuracy: {accuracy:.4f}")
                    
                    # Update best model if this one is better
                    if cv_score.mean() > self.best_accuracy:
                        self.best_accuracy = cv_score.mean()
                        self.best_model = best_model
                        self.best_model_name = name
                        
                except Exception as e:
                    logger.error(f"Error training {name}: {str(e)}")
                    accuracies[name] = 0.0
                    cv_scores[name] = 0.0
            
            self.cv_scores = cv_scores
            
            # Create ensemble models
            self._create_advanced_ensemble(X_train_scaled, y_train, X_test_scaled, y_test)
            
            # Save the best model
            self._save_best_model()
            
            return accuracies
            
        except Exception as e:
            logger.error(f"Error in training: {str(e)}")
            raise
    
    def _create_advanced_ensemble(self, X_train: np.ndarray, y_train: np.ndarray, 
                                X_test: np.ndarray, y_test: np.ndarray):
        """
        Create advanced ensemble models.
        
        Args:
            X_train (np.ndarray): Training features
            y_train (np.ndarray): Training targets
            X_test (np.ndarray): Test features
            y_test (np.ndarray): Test targets
        """
        try:
            # Get top performing models (CV score > 0.75)
            good_models = []
            for name, model in self.models.items():
                if name in self.cv_scores and self.cv_scores[name] > 0.75:
                    good_models.append((name, model))
            
            if len(good_models) >= 2:
                # Voting Classifier (Soft voting)
                voting_clf = VotingClassifier(
                    estimators=good_models,
                    voting='soft'
                )
                voting_clf.fit(X_train, y_train)
                
                # Evaluate voting classifier
                y_pred_voting = voting_clf.predict(X_test)
                voting_accuracy = accuracy_score(y_test, y_pred_voting)
                
                self.models['voting_ensemble'] = voting_clf
                
                # Update best model if ensemble is better
                if voting_accuracy > self.best_accuracy:
                    self.best_accuracy = voting_accuracy
                    self.best_model = voting_clf
                    self.best_model_name = 'voting_ensemble'
                
                logger.info(f"Voting Ensemble - Accuracy: {voting_accuracy:.4f}")
                
                # Stacking Ensemble (if we have enough models)
                if len(good_models) >= 3:
                    from sklearn.ensemble import StackingClassifier
                    
                    # Use logistic regression as meta-learner
                    stacking_clf = StackingClassifier(
                        estimators=good_models[:3],  # Use top 3 models
                        final_estimator=LogisticRegression(random_state=42),
                        cv=3
                    )
                    stacking_clf.fit(X_train, y_train)
                    
                    y_pred_stacking = stacking_clf.predict(X_test)
                    stacking_accuracy = accuracy_score(y_test, y_pred_stacking)
                    
                    self.models['stacking_ensemble'] = stacking_clf
                    
                    if stacking_accuracy > self.best_accuracy:
                        self.best_accuracy = stacking_accuracy
                        self.best_model = stacking_clf
                        self.best_model_name = 'stacking_ensemble'
                    
                    logger.info(f"Stacking Ensemble - Accuracy: {stacking_accuracy:.4f}")
            
        except Exception as e:
            logger.error(f"Error creating ensemble: {str(e)}")
    
    def _save_best_model(self):
        """Save the best performing model and preprocessors to disk."""
        try:
            if self.best_model is not None:
                model_path = os.path.join(self.model_save_path, 'enhanced_best_model.pkl')
                scaler_path = os.path.join(self.model_save_path, 'enhanced_scaler.pkl')
                metadata_path = os.path.join(self.model_save_path, 'enhanced_metadata.pkl')
                
                joblib.dump(self.best_model, model_path)
                joblib.dump(self.scaler, scaler_path)
                
                # Save metadata
                metadata = {
                    'best_model_name': self.best_model_name,
                    'best_accuracy': self.best_accuracy,
                    'cv_scores': self.cv_scores,
                    'feature_names': self.text_processor.get_feature_names()
                }
                joblib.dump(metadata, metadata_path)
                
                logger.info(f"Enhanced model saved: {self.best_model_name} (Accuracy: {self.best_accuracy:.4f})")
                
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
    
    def get_comprehensive_evaluation(self) -> Dict[str, Any]:
        """
        Get comprehensive evaluation metrics for all models.
        
        Returns:
            Dict[str, Any]: Comprehensive performance metrics
        """
        try:
            X, y = self.load_and_preprocess_data()
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            X_train = X_train.fillna(X_train.median())
            X_test = X_test.fillna(X_train.median())
            
            X_test_scaled = self.scaler.transform(X_test)
            
            evaluation = {}
            
            for name, model in self.models.items():
                try:
                    y_pred = model.predict(X_test_scaled)
                    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1] if hasattr(model, 'predict_proba') else None
                    
                    # Basic metrics
                    accuracy = accuracy_score(y_test, y_pred)
                    f1 = f1_score(y_test, y_pred)
                    
                    # Classification report
                    report = classification_report(y_test, y_pred, output_dict=True)
                    
                    # ROC AUC if probabilities available
                    roc_auc = roc_auc_score(y_test, y_pred_proba) if y_pred_proba is not None else None
                    
                    evaluation[name] = {
                        'accuracy': accuracy,
                        'f1_score': f1,
                        'precision': report['weighted avg']['precision'],
                        'recall': report['weighted avg']['recall'],
                        'roc_auc': roc_auc,
                        'cv_score': self.cv_scores.get(name, 0.0),
                        'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
                    }
                    
                except Exception as e:
                    logger.error(f"Error evaluating {name}: {str(e)}")
                    evaluation[name] = {'error': str(e)}
            
            return evaluation
            
        except Exception as e:
            logger.error(f"Error in comprehensive evaluation: {str(e)}")
            return {}
    
    def predict_with_confidence(self, input_data: List) -> Tuple[int, float, Dict]:
        """
        Make prediction with confidence and additional metrics.
        
        Args:
            input_data (List): List of input features
            
        Returns:
            Tuple[int, float, Dict]: Prediction, confidence, and additional info
        """
        try:
            if self.best_model is None:
                raise ValueError("No trained model available. Please train the model first.")
            
            # Preprocess input
            input_array = self.text_processor.preprocess_for_prediction(input_data)
            
            # Convert to DataFrame for feature engineering
            feature_names = self.text_processor.get_feature_names()
            input_df = pd.DataFrame(input_array, columns=feature_names)
            
            # Apply same feature engineering as training
            input_df = self._engineer_features(input_df)
            
            # Handle missing values
            input_df = input_df.fillna(0)  # Simple imputation for prediction
            
            # Scale input
            input_scaled = self.scaler.transform(input_df.values)
            
            # Make prediction
            prediction = self.best_model.predict(input_scaled)[0]
            
            # Get confidence and probabilities
            additional_info = {
                'model_used': self.best_model_name,
                'model_accuracy': self.best_accuracy
            }
            
            if hasattr(self.best_model, 'predict_proba'):
                probabilities = self.best_model.predict_proba(input_scaled)[0]
                confidence = max(probabilities)
                additional_info['probabilities'] = {
                    'healthy': probabilities[0],
                    'disease': probabilities[1]
                }
            else:
                confidence = 0.85  # Default confidence
            
            return int(prediction), confidence, additional_info
            
        except Exception as e:
            logger.error(f"Error in prediction: {str(e)}")
            raise
