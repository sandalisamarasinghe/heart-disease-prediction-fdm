"""
Training Script for Heart Disease Prediction Model
Trains the model using unstructured text data from heart.txt
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from heart_disease_model import HeartDiseaseModel
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """
    Main training function.
    """
    try:
        # Path to the text file
        text_file_path = '/Users/hirushathisayuruellawala/Downloads/FDM Assignment/Heart-Disease-Prediction-System-main/data/heart.txt'
        
        # Check if text file exists
        if not os.path.exists(text_file_path):
            logger.error(f"Text file not found: {text_file_path}")
            return
        
        logger.info("Starting Heart Disease Model Training...")
        logger.info(f"Using text file: {text_file_path}")
        
        # Initialize model
        model = HeartDiseaseModel(
            text_file_path=text_file_path,
            model_save_path='apps/ml/models/'
        )
        
        # Train models
        logger.info("Training models...")
        accuracies = model.train_models(test_size=0.2, random_state=42)
        
        # Display results
        logger.info("\n" + "="*50)
        logger.info("TRAINING RESULTS")
        logger.info("="*50)
        
        for model_name, accuracy in accuracies.items():
            logger.info(f"{model_name.upper()}: {accuracy:.4f} ({accuracy*100:.2f}%)")
        
        # Get best model info
        if model.best_model is not None:
            logger.info(f"\nBest Model: {type(model.best_model).__name__}")
            logger.info(f"Best Accuracy: {model.best_accuracy:.4f} ({model.best_accuracy*100:.2f}%)")
        
        # Get detailed performance metrics
        logger.info("\nGetting detailed performance metrics...")
        performance = model.get_model_performance()
        
        logger.info("\n" + "="*50)
        logger.info("DETAILED PERFORMANCE METRICS")
        logger.info("="*50)
        
        for model_name, metrics in performance.items():
            if 'error' not in metrics:
                logger.info(f"\n{model_name.upper()}:")
                logger.info(f"  Accuracy: {metrics['accuracy']:.4f}")
                logger.info(f"  Precision: {metrics['precision']:.4f}")
                logger.info(f"  Recall: {metrics['recall']:.4f}")
                logger.info(f"  F1-Score: {metrics['f1_score']:.4f}")
            else:
                logger.error(f"{model_name}: {metrics['error']}")
        
        # Get feature importance
        logger.info("\nGetting feature importance...")
        feature_importance = model.get_feature_importance()
        
        if feature_importance:
            logger.info("\n" + "="*50)
            logger.info("FEATURE IMPORTANCE")
            logger.info("="*50)
            
            # Sort features by importance
            sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
            
            for feature, importance in sorted_features:
                logger.info(f"{feature}: {importance:.4f}")
        
        # Test prediction with sample data
        logger.info("\nTesting prediction with sample data...")
        try:
            # Sample input data (13 features)
            sample_input = [63, 0, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1]
            
            prediction, confidence = model.predict(sample_input)
            
            logger.info(f"Sample Prediction: {prediction} (0=Healthy, 1=Disease)")
            logger.info(f"Confidence: {confidence:.4f}")
            
        except Exception as e:
            logger.error(f"Error testing prediction: {str(e)}")
        
        logger.info("\nTraining completed successfully!")
        logger.info("Model saved to: models/")
        
    except Exception as e:
        logger.error(f"Training failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
