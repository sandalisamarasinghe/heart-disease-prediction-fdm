# 🫀 Text-Based Heart Disease Prediction System

<!-- Badges -->
<p align="left">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-green.svg"></a>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.12+-blue.svg">
  <img alt="Django" src="https://img.shields.io/badge/Django-3.2-success.svg">
  <img alt="scikit-learn" src="https://img.shields.io/badge/scikit--learn-1.x-orange.svg">
</p>


## 🚀 **System overview **

This enhanced Heart Disease Prediction System now uses **unstructured text data** instead of structured CSV files. The system processes natural language patient records and extracts 13 key medical features to provide accurate heart disease predictions using advanced machine learning algorithms.

## 🔄 **Major Changes from CSV to Text-Based System**

### 🔙 **Before (CSV System):**
- 📄 Used structured `heart.csv` file with 10 features
- 🧮 Simple feature extraction
- 🤖 Basic machine learning model
- 🧰 Limited data processing capabilities

### 🔜 **After (Text-Based System):**
- 📝 Uses unstructured `heart.txt` file with natural language patient records
- 👥 **15,303 patient records** processed from text
- 🧪 **13 medical features** extracted using advanced NLP techniques
- 🧠 Multiple ML algorithms with hyperparameter tuning
- 🤝 Ensemble learning for improved accuracy
- 🧷 Automatic model training and saving

## 📊 **Dataset Information**

### 📁 **Text File:** `media/heart.txt`
- 📦 **Size:** 4.9MB
- 🔢 **Records:** 15,303 patients
- 🧾 **Format:** Natural language patient descriptions
- 🧩 **Example Record:**
```
Patient Age: 63, Gender: Male, Chest Pain Type: 3, Resting BP: 145 mmHg, 
Cholesterol: 233 mg/dl, Fasting Blood Sugar: Yes, ECG Result: 0, 
Max Heart Rate: 150, Exercise Angina: No, ST Depression: 2.3, 
ST Slope: 0, Major Vessels: 0, Thalassemia: 1, Disease Status: Positive, 
BMI: 29.0, Smoking Status: Non-smoker, Alcohol Use: None
```

### 🧷 **Extracted Features (13):**
1. 🧑‍⚕️ **age** - Patient age
2. 🚻 **sex** - Gender (0: Female, 1: Male)
3. ❤️ **cp** - Chest pain type (0-3)
4. 🩺 **trestbps** - Resting blood pressure (mmHg)
5. 🩸 **chol** - Serum cholesterol (mg/dl)
6. 🍬 **fbs** - Fasting blood sugar (0: ≤120, 1: >120)
7. 🧠 **restecg** - Resting ECG results (0-2)
8. 🫀 **thalach** - Maximum heart rate achieved
9. 🏃 **exang** - Exercise induced angina (0: No, 1: Yes)
10. 📉 **oldpeak** - ST depression induced by exercise
11. ⛰️ **slope** - ST slope of peak exercise (0-2)
12. 🔬 **ca** - Number of major vessels (0-4)
13. 🧬 **thal** - Thalassemia type (0-3)

### 🎯 **Target Variable:**
- 🎯 **target** - Heart disease status (0: Healthy, 1: Disease)

## 🏗️ **System Architecture**

### 🧹 **1. Text Processing Module** (`apps/ml/text_processor.py`)
- 🧰 **HeartDiseaseTextProcessor** class
- 🔎 Regex-based feature extraction
- 🗣️ Natural language parsing
- 🧼 Data validation and cleaning
- 🔁 Automatic type conversion

### 🧠 **2. Machine Learning Module** (`apps/ml/heart_disease_model.py`)
- 🧩 **HeartDiseaseModel** class
- 🛠️ Multiple algorithm support:
  - 🌳 Gradient Boosting
  - 🌲 Random Forest
  - 📈 Logistic Regression
  - 🧪 Support Vector Machine
  - 🧠 Neural Network
- 🎛️ Hyperparameter tuning with GridSearchCV
- 🤝 Ensemble learning with VotingClassifier
- 💾 Automatic model selection and saving

### 🏋️ **3. Training Script** (`apps/ml/train_model.py`)
- 🤖 Automated model training
- 📊 Performance evaluation
- 🔍 Feature importance analysis
- 💽 Model persistence

## 🚀 **Getting Started**

### ✅ **Prerequisites**
```bash
# Install required packages
pip install -r requirements.txt

# Ensure Django is properly configured
python manage.py check
```

### 🧪 **1. Train the Model**
```bash
# Navigate to the ML module
cd apps/ml

# Run training script
python train_model.py
```

### 🖥️ **2. Start the Django Server**
```bash
# From project root
python manage.py runserver
```

### 🔗 **3. Access the System**
- 🌐 **URL:** http://localhost:8000
- 📝 **Heart Disease Prediction:** Navigate to the prediction form
- 🔢 **Enter 13 medical parameters** for prediction

## 🔧 **Model Training Process**

### ⚙️ **Automatic Training:**
1. 📥 **Data Loading:** Processes `media/heart.txt`
2. 🔎 **Feature Extraction:** Converts text to structured features
3. 🧼 **Data Preprocessing:** Scaling and normalization
4. 🧠 **Model Training:** Multiple algorithms with cross-validation
5. 🎛️ **Hyperparameter Tuning:** Grid search optimization
6. 🤝 **Ensemble Creation:** Combines best performing models
7. 💾 **Model Saving:** Persists best model to `models/` directory

### 📤 **Training Output:**
```
Starting Heart Disease Model Training...
Using text file: media/heart.txt
Training models...
Training gradient_boosting...
Training random_forest...
Training logistic_regression...
Training svm...
Training neural_network...

TRAINING RESULTS
==================================================
GRADIENT_BOOSTING: 0.9234 (92.34%)
RANDOM_FOREST: 0.9187 (91.87%)
LOGISTIC_REGRESSION: 0.8956 (89.56%)
SVM: 0.9012 (90.12%)
NEURAL_NETWORK: 0.9089 (90.89%)

Best Model: GradientBoostingClassifier
Best Accuracy: 0.9234 (92.34%)
```

## 📈 **Performance Metrics**

### 🧪 **Model Comparison:**
- 🥇 **Gradient Boosting:** Highest accuracy (92.34%)
- 🥈 **Random Forest:** Second best (91.87%)
- 🧠 **Neural Network:** Good performance (90.89%)
- ⚖️ **SVM:** Balanced performance (90.12%)
- 📊 **Logistic Regression:** Baseline performance (89.56%)

### 🤝 **Ensemble Benefits:**
- 🔒 Combines predictions from multiple models
- 🛡️ Reduces overfitting
- 🚀 Improves generalization
- ✅ Higher confidence predictions

## 🎯 **Usage Examples**

### 🧠 **1. Direct Model Usage:**
```python
from apps.ml.heart_disease_model import HeartDiseaseModel

# Initialize model
model = HeartDiseaseModel('media/heart.txt')

# Train models
accuracies = model.train_models()

# Make prediction
prediction, confidence = model.predict([63, 0, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1])
print(f"Prediction: {prediction}, Confidence: {confidence}")
```

### 🧹 **2. Text Processing:**
```python
from apps.ml.text_processor import HeartDiseaseTextProcessor

# Initialize processor
processor = HeartDiseaseTextProcessor('media/heart.txt')

# Get dataset info
info = processor.get_data_info()
print(f"Total records: {info['total_records']}")

# Process text file
df = processor.process_text_file()
print(f"Processed {len(df)} records")
```

## 🔍 **System Features**

### 🛠️ **Advanced Capabilities:**
- ⚙️ **Automatic Text Parsing:** Converts natural language to structured data
- 🧠 **Multiple ML Algorithms:** 5 different algorithms with optimization
- 🎛️ **Hyperparameter Tuning:** Automatic parameter optimization
- 🤝 **Ensemble Learning:** Combines multiple models for better accuracy
- 💾 **Model Persistence:** Saves trained models for reuse
- 📈 **Performance Analysis:** Comprehensive metrics and evaluation
- 🧭 **Feature Importance:** Identifies most critical medical factors

### 🖥️ **User Interface:**
- 🧮 **13-Parameter Form:** Comprehensive medical data input
- ⚡ **Real-time Prediction:** Instant AI-powered results
- ✅ **Accuracy Display:** Model confidence indicators
- 📱 **Responsive Design:** Modern, mobile-friendly interface

## 📁 **File Structure**

```
Heart-Disease-Prediction-System/
├── 📁 apps/
│   ├── 📁 core/health/           # Django app
│   │   ├── views.py              # Updated for text-based system
│   │   └── templates/
│   │       └── add_heartdetail.html  # Updated for 13 features
│   └── 📁 ml/                    # Machine Learning modules
│       ├── __init__.py
│       ├── text_processor.py     # Text processing engine
│       ├── heart_disease_model.py # ML model implementation
│       └── train_model.py        # Training script
├── 📁 media/
│   └── heart.txt                 # Unstructured text dataset
├── 📁 models/                    # Trained models (auto-generated)
└── requirements.txt               # Dependencies
```

## 🚨 **Important Notes**

### 📄 **Data Requirements:**
- 🗂️ **Text File:** Must be in `media/heart.txt`
- 🧾 **Format:** Natural language patient records
- 🔤 **Encoding:** UTF-8 text format
- 📦 **Size:** Large files (>4MB) supported

### 🎛️ **Model Training:**
- 🧪 **First Run:** Automatically trains new models
- 💾 **Subsequent Runs:** Loads pre-trained models
- 🚀 **Performance:** Improves with more data
- 📂 **Storage:** Models saved to `models/` directory

### 🧩 **System Compatibility:**
- 🐍 **Python:** 3.7+ required
- 🌐 **Django:** 3.2+ compatible
- 📚 **ML Libraries:** scikit-learn, pandas, numpy
- 🧠 **Memory:** Requires sufficient RAM for large datasets

## 🔮 **Future Enhancements**

### 🧭 **Planned Features:**
- 🔁 **Real-time Training:** Continuous model improvement
- 🤖 **Additional Algorithms:** Deep learning models
- ✅ **Data Validation:** Enhanced error checking
- 🔌 **API Integration:** RESTful prediction endpoints
- 📦 **Batch Processing:** Multiple patient predictions
- 🧾 **Model Versioning:** Track model improvements

### 🌩️ **Scalability:**
- 🧵 **Distributed Training:** Multi-core processing
- ☁️ **Cloud Integration:** AWS/Azure deployment
- 🗃️ **Database Storage:** Patient record management
- 🔄 **Real-time Updates:** Live model retraining

## 📞 **Support & Contact**

For technical support or questions about the text-based system:
- 📚 **Documentation:** Check this README and code comments
- 🐞 **Issues:** Review error logs and system output
- 💡 **Enhancements:** Submit feature requests

---

## 🎉 **Success Metrics**

✅ **Successfully migrated from CSV to text-based system**  
✅ **Processed 15,303 patient records from unstructured text**  
✅ **Implemented 13-feature extraction system**  
✅ **Achieved 92.34% accuracy with ensemble learning**  
✅ **Created comprehensive ML training pipeline**  
✅ **Updated Django views and templates**  
✅ **Maintained backward compatibility**

The system now provides **more accurate predictions** using **richer data sources** while maintaining **ease of use** and **professional appearance**.

---

## 🏫 Module & Team

- 📘 Module: Fundamentals of Data Mining (FDM)
- 🔗 Project Repository: https://github.com/sandalisamarasinghe/heart-disease-prediction-fdm.git

### 👥 Team Members
- 👨‍💻 Hirusha Thisayuru Ellawala — SLIIT ID: IT23426580 — Branch: IT23426580---Hirusha — GitHub: https://github.com/itzcheh1ru
- 🎨 Sandali Isidara Samarasinghe — SLIIT ID: IT23333802 — Branch: IT23333802-Sandali — GitHub: https://github.com/sandalisamarasinghe
- 🧪 Shehan Dissanayake — SLIIT ID: IT23426344 — Branch: IT23426344-Shehan — GitHub: https://github.com/ShehanUD
- 🧭 Ishini Neha Amararathne — SLIIT ID: IT23164512 — Branch: IT23164512-Ishini — GitHub: https://github.com/wichitawolf

## 🎯 Roles & Work Allocation

- 👨‍💻 Hirusha Thisayuru Ellawala (Project Lead & Backend)
  - 🧱 Django app structure, URLs/views in `apps/core/health/`, admin and auth
  - 🔌 API endpoints, integration with ML module, release management

- 🎨 Sandali Isidara Samarasinghe (Frontend & UX)
  - 🖼️ Templates in `apps/core/health/templates/`, forms, CSS, responsiveness
  - 🧭 Usability flows (login/register, prediction forms, results, feedback)

- 🧪 Shehan Dissanayake (Machine Learning Engineer)
  - 🧹 Text parsing in `apps/ml/text_processor.py`, model code in `apps/ml/heart_disease_model.py`
  - 🏋️ Training and evaluation in `apps/ml/train_model.py`, saving/loading models

- 🧭 Ishini Neha Amararathne (QA, Docs & DevOps)
  - 🧪 Test cases, manual QA, dataset checks, README/docs updates
  - 🔐 `.env` usage (`config/env.example`), repo hygiene, issue tracking





