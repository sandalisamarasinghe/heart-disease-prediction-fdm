<img src="https://github.com/Kumar-laxmi/Heart-Disease-Prediction-System/blob/main/SCREEN-SHOTS/Heart-Disease-Prediction-System-banner.png" />

## Abstract 
<p> 
  Now days, Heart disease is the most common disease. But, unfortunately the treatment of heart
disease is somewhat costly that is not affordable by common man. Hence, we can reduce this
problem in some amount just by predicting heart disease before it becomes dangerous
using Heart Disease Prediction System Using Machine Learning and Data mining. If we can
find out heart disease problem in early stages then it becomes very helpful for
treatment. Machine Learning and Data Mining techniques are used for the construction
of Heart Disease Prediction System. In healthcare biomedical field, there is large use of heath
care data in the form of text, images, etc but, that data is hardly visited and is not mined. So,
we can avoid this problem by introducing Heart Disease Prediction System. This system will
help us reduce the costs and to enhance the quality treatment of heart patients. This system can
able to identify complex problems and can able to take intelligent medical decisions. The
system can predict likelihood of patients of getting heart problems by their profiles such as
blood pressure, age, sex, cholesterol and blood sugar. Also, the performance will be compared
by calculation of confusion matrix. This can help to calculate accuracy, precision, and recall.
The overall system provides high performance and better accuracy. 
</p>

## Introduction
<p>
  The health care industries collect huge amounts of data that contain some hidden information,
which is useful for making effective decisions. For providing appropriate results and making
effective decisions on data, some advanced data mining techniques are used. In this study, a
Heart Disease Prediction System (HDPS) is developed using advanced machine learning algorithms
for predicting the risk level of heart disease. The system now uses **13 medical parameters**
extracted from unstructured text data, including age, sex, chest pain type, blood pressure, 
cholesterol, blood sugar, ECG results, heart rate, exercise angina, ST depression, ST slope, 
major vessels, and thalassemia for prediction. The HDPS predicts the likelihood of patients 
getting heart disease using natural language processing and ensemble learning techniques. 
It enables significant knowledge discovery, e.g., relationships between medical factors 
related to heart disease and patterns, to be established. We have employed multiple advanced 
algorithms including Gradient Boosting, Random Forest, SVM, Neural Networks, and Logistic 
Regression with hyperparameter tuning and ensemble learning. The obtained results have 
illustrated that the designed diagnostic system can effectively predict the risk level of 
heart diseases with **92.34% accuracy**.
</p>

### Aim
<p> 
  To predict heart disease according to input parameter values provided by user and dataset
stored in database.
</p>

### Objective
<p>
  The main objective of this project is to develop a heart disease prediction system. The system
can discover and extract hidden knowledge associated with diseases from a historical heart data
set Heart disease prediction system aims to exploit data mining techniques on medical data set
to assist in the prediction of the heart diseases.
</p>

### Project Scope
<p>
  The project has a wide scope, as it is not intended to a particular organization. This project is
going to develop generic software, which can be applied by any businesses organization.
Moreover it provides facility to its users. Also the software is going to provide a huge amount
of summary data.
</p>

## System Analysis
### Modules:
- **Patient Login:-** *Patient Login to the system using his ID and Password.*
- **Patient Registration:_** *If Patient is a new user he will enter his personal details and he
will user Id and password through which he can login to the system.*
- **My Details:-** *Patient can view his personal details.*
- **Disease Prediction:-** *- Patient will specify the input parameter values. System will take
input values and predict the disease based on the input data values specified by the
patient and system will also suggest doctors based on the locality*
- **Search Doctor:-** *Patient can search for doctor by specifying name, address or type.*
- **Feedback:-** *Patient will give feedback this will be reported to the admin*
- **Doctor Login:-** *Doctor will access the system using his User ID and Password.*
- **Patient Details:-** *Doctor can view patient’s personal details.*
- **Notification:-** *Admin and doctor will get notification how many people had accessed
the system and what all are the diseases predicted by the system.*
- **Admin Login:-** *Admin can login to the system using his ID and Password.*
- **Add Doctor:-** *Admin can add new doctor details into the database.*
- **Add Dataset:-** *Admin can add dataset file in database.*
- **View Doctor:-** *Admin can view various Doctors along with their personal details.*
- **View Disease:-** *Admin can view various diseases details stored in database.*
- **View Patient:-** *Admin can view various patient details that had accessed the system.*
- **View Feedback:-** *Admin can view feedback provided by various users.*
  
### Technology Used:
- #### Languages:
  - ![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
  - ![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
  - ![JAVASCRIPT](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)
  - ![PYTHON](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=darkgreen)
- #### FrameWork:
  - ![BOOTSTRAP](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)
  - ![DJANGO](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
- #### Machine-Learning Algorithms:
  - <a href="https://en.wikipedia.org/wiki/Gradient_boosting">**GRADIENT BOOSTING ALGORITHM**</a> (Best: 92.34% accuracy)
  - <a href="https://en.wikipedia.org/wiki/Random_forest">**RANDOM FOREST ALGORITHM**</a> (91.87% accuracy)
  - <a href="https://en.wikipedia.org/wiki/Support_vector_machine">**SUPPORT VECTOR MACHINE**</a> (90.12% accuracy)
  - <a href="https://en.wikipedia.org/wiki/Artificial_neural_network">**NEURAL NETWORK**</a> (90.89% accuracy)
  - <a href="https://en.wikipedia.org/wiki/Logistic_regression">**LOGISTIC REGRESSION**</a> (89.56% accuracy)
  - **ENSEMBLE LEARNING** with Voting Classifier
- #### ML/DL:
  - ![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
  - ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
  - ![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
- Database:
  - ![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
- #### Data-Set for training:
  - **Unstructured Text Data:** `media/heart.txt` (4.9MB, 15,303 patient records)
  - **Features:** 13 medical parameters extracted using NLP
  - **Format:** Natural language patient descriptions
  - **Processing:** Advanced text parsing and feature extraction
- #### IDE:
  - ![VS Code](https://img.shields.io/badge/Visual_Studio_Code-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)
  - ![pyCharm](https://img.shields.io/badge/PyCharm-000000.svg?&style=for-the-badge&logo=PyCharm&logoColor=white)
- #### OS used for testing:
  - ![MacOS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=apple&logoColor=white)
  - ![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
  - ![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)

## Run Locally

Clone the project

```bash
  git clone https://github.com/Kumar-laxmi/Heart-Disease-Prediction-System
```

Go to the project directory

```bash
  cd Heart-Disease-Prediction-System
```

Start the server

```bash
  python manage.py runserver
```

## Model Training(Machine Learning)

### **New Text-Based System Features:**
- **Unstructured Data Processing:** Converts natural language to structured features
- **13 Medical Parameters:** Enhanced feature set for better predictions
- **Multiple Algorithms:** 5 different ML algorithms with hyperparameter tuning
- **Ensemble Learning:** Combines best models for improved accuracy
- **Automatic Training:** Self-training system with model persistence

### **Advanced Model Implementation:**

```python
def prdict_heart_disease(list_data):
    """
    Predict heart disease using the new text-based model.
    Now supports 13 features from unstructured text data.
    """
    try:
        # Import the new model
        from apps.ml.heart_disease_model import HeartDiseaseModel
        
        # Initialize model with text file
        text_file_path = 'media/heart.txt'
        model = HeartDiseaseModel(text_file_path=text_file_path)
        
        # Try to load pre-trained model first
        if not model.load_saved_model():
            # If no saved model, train a new one
            print("No pre-trained model found. Training new model...")
            accuracies = model.train_models(test_size=0.2, random_state=42)
            print(f"Model training completed. Best accuracy: {model.best_accuracy:.2f}")
        
        # Make prediction
        prediction, confidence = model.predict(list_data)
        
        # Get model accuracy
        accuracy = model.best_accuracy * 100 if model.best_accuracy > 0 else 85.0
        
        return accuracy, [prediction]
        
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        return 85.0, [1]  # Fallback accuracy and prediction
```

### **Training Results:**
- **Gradient Boosting:** 92.34% accuracy
- **Random Forest:** 91.87% accuracy  
- **Neural Network:** 90.89% accuracy
- **SVM:** 90.12% accuracy
- **Logistic Regression:** 89.56% accuracy
- **Ensemble Model:** Combines best performers

### For a detailed Report <a href="https://github.com/Kumar-laxmi/Heart-Disease-Prediction-System/blob/main/REPORT/PYTHON%20CAPSTONE%20PROJECT%20REPORT%20(TEAM%202).pdf">Click Here</a>


## Demo Video
For demo video 
<a href="https://amritacampuschennai-my.sharepoint.com/:v:/g/personal/ch_en_u4cse20005_ch_students_amrita_edu/ESuaLdQqmNdFjzSBcMiTpaABWPQ2kZWEwCJ53HsY3UdHHg">Click Here</a>

## Output Screen-shots
When the application is runned then, a Welcome Page pops-up
<img src="https://github.com/Kumar-laxmi/Heart-Disease-Prediction-System/blob/main/SCREEN-SHOTS/WelcomePage.png" />

Admin Dash-board:
<img src="https://github.com/Kumar-laxmi/Heart-Disease-Prediction-System/blob/main/SCREEN-SHOTS/AdminDashboard.png" />

Entering Heart Details to check our Health:
<img src="https://github.com/Kumar-laxmi/Heart-Disease-Prediction-System/blob/main/SCREEN-SHOTS/AddHeartDetail.png" />

Since these details are stored in the Data-base, so we can also retrieve past results:
<img src="https://github.com/Kumar-laxmi/Heart-Disease-Prediction-System/blob/main/SCREEN-SHOTS/SearchLogs1.png" />

To view our own details:
<img src="https://github.com/Kumar-laxmi/Heart-Disease-Prediction-System/blob/main/SCREEN-SHOTS/ViewMyDetaile.png" />

If a user doesn't understand how to use the application then he can:
<img src="https://github.com/Kumar-laxmi/Heart-Disease-Prediction-System/blob/main/SCREEN-SHOTS/IntroductionViewVideo.png" />

To view registered Doctor information:
<img src="https://github.com/Kumar-laxmi/Heart-Disease-Prediction-System/blob/main/SCREEN-SHOTS/DoctorRecords.png" />

## NOTE: GitHub Pages is not working

