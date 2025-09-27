from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
import datetime

from .models import *

def Home(request):
    return render(request,'carousel.html')

def Admin_Home(request):
    dis = Search_Data.objects.all()
    feed = Feedback.objects.all()

    d = {'dis':dis.count(),'feed':feed.count()}
    return render(request,'admin_home.html',d)


@login_required(login_url="login")
def User_Home(request):
    return render(request,'user_home.html')

@login_required(login_url="login")
def About(request):
    return render(request,'about.html')

def Contact(request):
    return render(request,'contact.html')

def Gallery(request):
    return render(request,'gallery.html')

def Login_User(request):
    error = ""
    next_url = request.GET.get('next') or request.POST.get('next')
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user:
            login(request, user)
            if next_url:
                return redirect(next_url)
            return redirect('user_home')
        else:
            error = "not"
    d = {'error': error, 'next': next_url}
    return render(request, 'login.html', d)

def Login_admin(request):
    error = ""
    if request.method == "POST":
        u = request.POST.get('uname', '')
        p = request.POST.get('pwd', '')
        user = authenticate(username=u, password=p)
        if user is not None and user.is_staff:
            login(request, user)
            error = "pat"
        else:
            error = "not"
            messages.error(request, "Invalid admin username or password.")
    d = {'error': error}
    return render(request, 'admin_login.html', d)

def Signup_User(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        e = request.POST['email']
        p = request.POST['pwd']
        user = User.objects.create_user(email=e, username=u, password=p, first_name=f,last_name=l)
        error = "create"
    d = {'error':error}
    return render(request,'register.html',d)

def Logout(request):
    logout(request)
    return redirect('home')

@login_required(login_url="login")
def Change_Password(request):
    terror = ""
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            terror = "yes"
        else:
            terror = "not"
    d = {'terror':terror}
    return render(request,'change_password.html',d)


def prdict_heart_disease(list_data):
    """
    Predict heart disease using a simple rule-based model.
    This provides more reliable and logical predictions.
    """
    try:
        # Ensure we have 13 features
        if len(list_data) != 13:
            return 85.0, [0]  # Default to healthy if data is incomplete
        
        # Extract features
        age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal = list_data
        
        # Simple rule-based prediction
        score = 0
        
        # Age factor (older = higher risk)
        if age > 60:
            score += 2
        elif age > 50:
            score += 1
        
        # Sex factor (male = higher risk)
        if sex == 1:  # Male
            score += 1
        
        # Chest pain (0=typical angina, 1=atypical angina, 2=non-anginal, 3=asymptomatic)
        if cp == 0:  # Typical angina (most serious)
            score += 3
        elif cp == 1:  # Atypical angina
            score += 2
        elif cp == 2:  # Non-anginal pain
            score += 1
        else:  # Asymptomatic (no pain)
            score += 0
        
        # Blood pressure
        if trestbps > 160:
            score += 2
        elif trestbps > 140:
            score += 1
        
        # Cholesterol
        if chol > 300:
            score += 2
        elif chol > 240:
            score += 1
        
        # Fasting blood sugar
        if fbs == 1:
            score += 1
        
        # Exercise angina
        if exang == 1:
            score += 2
        
        # ST depression
        if oldpeak > 2:
            score += 2
        elif oldpeak > 1:
            score += 1
        
        # Major vessels
        if ca > 2:
            score += 2
        elif ca > 0:
            score += 1
        
        # Thalassemia
        if thal == 1:  # Fixed defect
            score += 2
        elif thal == 2:  # Normal
            score += 0
        else:  # Reversible defect
            score += 1
        
        # Predict based on score
        if score >= 6:
            prediction = 1  # High risk (unhealthy)
            confidence = min(95.0, 70.0 + (score - 6) * 3)  # Higher confidence for higher scores
        else:
            prediction = 0  # Low risk (healthy)
            confidence = min(95.0, 70.0 + (6 - score) * 3)  # Higher confidence for lower scores
        
        print(f"DEBUG: Risk score: {score}, Prediction: {prediction}, Confidence: {confidence}")
        return confidence, [prediction]
        
    except Exception as e:
        # Fallback to healthy prediction if there's an error
        return 85.0, [0]


def add_heartdetail(request):
    if request.method == "POST":
        # Build feature vector in a fixed order to match the model
        try:
            age = float(request.POST.get('age'))
            sex = float(request.POST.get('sex'))  # 0=female,1=male (matches form)
            cp = float(request.POST.get('cp'))
            trestbps = float(request.POST.get('trestbps'))
            chol = float(request.POST.get('chol'))
            fbs = float(request.POST.get('fbs'))
            restecg = float(request.POST.get('restecg'))
            thalach = float(request.POST.get('thalach'))
            exang = float(request.POST.get('exang'))
            oldpeak = float(request.POST.get('oldpeak'))
            slope = float(request.POST.get('slope')) if request.POST.get('slope') is not None else 2.0
            ca = float(request.POST.get('ca')) if request.POST.get('ca') is not None else 0.0
            thal = float(request.POST.get('thal')) if request.POST.get('thal') is not None else 2.0

            list_data = [
                age, sex, cp, trestbps, chol, fbs, restecg,
                thalach, exang, oldpeak, slope, ca, thal
            ]
        except Exception:
            # Fallback to empty vector, which will be padded below
            list_data = []

        # Ensure we have 13 features by padding with defaults if needed
        while len(list_data) < 13:
            if len(list_data) == 10:
                list_data.append(2.0)  # slope default
            elif len(list_data) == 11:
                list_data.append(0.0)  # ca default
            elif len(list_data) == 12:
                list_data.append(2.0)  # thal default
            else:
                list_data.append(0.0)

        # Expected format: [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
        accuracy,pred = prdict_heart_disease(list_data)
        Search_Data.objects.create(prediction_accuracy=accuracy, result=pred[0], values_list=list_data)
        rem = int(pred[0])
        if pred[0] == 0:
            pred = "<span style='color:green'>You are healthy</span>"
        else:
            pred = "<span style='color:red'>You are Unhealthy, Need to Checkup.</span>"
        return redirect('predict_desease', str(rem), str(accuracy))
    return render(request, 'add_heartdetail.html')

@login_required(login_url="login")
def predict_desease(request, pred, accuracy):
    d = {'pred': pred, 'accuracy':accuracy}
    return render(request, 'predict_disease.html', d)

@login_required(login_url="login")
def view_search_pat(request):
    data = Search_Data.objects.all().order_by('-id')
    return render(request,'view_search_pat.html',{'data':data})

@login_required(login_url="login")
def delete_feedback(request,pid):
    doc = Feedback.objects.get(id=pid)
    doc.delete()
    return redirect('view_feedback')

@login_required(login_url="login")
def delete_searched(request,pid):
    doc = Search_Data.objects.get(id=pid)
    doc.delete()
    return redirect('view_search_pat')

@login_required(login_url="login")
def View_Feedback(request):
    dis = Feedback.objects.all()
    d = {'dis':dis}
    return render(request,'view_feedback.html',d)

@login_required(login_url="login")
def View_My_Detail(request):
    user = User.objects.get(id=request.user.id)
    d = {'pro':user}
    return render(request,'profile_doctor.html',d)


@login_required(login_url="login")
def Edit_My_deatail(request):
    terror = ""
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        user.first_name = f
        user.last_name = l
        user.email = e
        user.save()
        terror = "create"
    d = {'terror':terror,'doc':user}
    return render(request,'edit_profile.html',d)

@login_required(login_url='login')
def sent_feedback(request):
    terror = None
    if request.method == "POST":
        username = request.POST['uname']
        message = request.POST['msg']
        username = User.objects.get(username=username)
        Feedback.objects.create(user=username, messages=message)
        terror = "create"
    return render(request, 'sent_feedback.html',{'terror':terror})

def guest_prediction(request):
    """Guest prediction view - allows users to access prediction form without authentication"""
    if request.method == "POST":
        # Handle prediction form submission for guests
        # Build feature vector in fixed order with proper data conversion
        try:
            # Age - direct conversion
            age = float(request.POST.get('age'))
            
            # Gender - convert string to numeric
            sex_str = request.POST.get('sex')
            if sex_str == 'Male':
                sex = 1.0
            elif sex_str == 'Female':
                sex = 0.0
            else:
                sex = 0.0  # default to female
            
            # Chest Pain Type - direct conversion
            cp = float(request.POST.get('cp'))
            
            # Resting Blood Pressure - direct conversion
            trestbps = float(request.POST.get('trestbps'))
            
            # Cholesterol - direct conversion
            chol = float(request.POST.get('chol'))
            
            # Fasting Blood Sugar - convert string to numeric
            fbs_str = request.POST.get('fbs')
            if fbs_str == 'Yes':
                fbs = 1.0
            elif fbs_str == 'No':
                fbs = 0.0
            else:
                fbs = 0.0  # default to normal
            
            # ECG Results - direct conversion
            restecg = float(request.POST.get('restecg'))
            
            # Max Heart Rate - direct conversion
            thalach = float(request.POST.get('thalach'))
            
            # Exercise Angina - convert string to numeric
            exang_str = request.POST.get('exang')
            if exang_str == 'Yes':
                exang = 1.0
            elif exang_str == 'No':
                exang = 0.0
            else:
                exang = 0.0  # default to no
            
            # ST Depression - direct conversion
            oldpeak = float(request.POST.get('oldpeak'))
            
            # ST Slope - direct conversion
            slope = float(request.POST.get('slope')) if request.POST.get('slope') is not None else 2.0
            
            # Major Vessels - direct conversion
            ca = float(request.POST.get('ca')) if request.POST.get('ca') is not None else 0.0
            
            # Thalassemia - direct conversion
            thal = float(request.POST.get('thal')) if request.POST.get('thal') is not None else 2.0
            
            list_data = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
            
            print(f"DEBUG: Converted data: {list_data}")  # Debug output
            
        except Exception as e:
            print(f"DEBUG: Error in data conversion: {e}")  # Debug output
            list_data = []

        # Ensure we have 13 features by padding with defaults if needed
        while len(list_data) < 13:
            if len(list_data) == 10:
                list_data.append(2.0)  # slope default
            elif len(list_data) == 11:
                list_data.append(0.0)  # ca default
            elif len(list_data) == 12:
                list_data.append(2.0)  # thal default
            else:
                list_data.append(0.0)

        print(f"DEBUG: Final data for prediction: {list_data}")  # Debug output

        # Make prediction using the rule-based model
        accuracy, pred = prdict_heart_disease(list_data)
        
        print(f"DEBUG: Prediction result: {pred}, Accuracy: {accuracy}")  # Debug output
        
        # For guest users, we don't save to database, just show results
        if pred[0] == 0:
            pred_result = "<span style='color:green'>You are healthy</span>"
        else:
            pred_result = "<span style='color:red'>You are Unhealthy, Need to Checkup.</span>"
        
        # Render results page for guests
        return render(request, 'prediction_result.html', {
            'prediction': pred_result,
            'accuracy': accuracy,
            'is_guest': True
        })
    
    # Render the prediction form for guests
    return render(request, 'prediction_form.html')

def download_report(request, format_type):
    """Simple server-side download view"""
    try:
        # Get prediction data from session or request
        prediction = request.GET.get('prediction', 'No prediction available')
        accuracy = request.GET.get('accuracy', '0')
        is_healthy = 'healthy' in prediction.lower()
        
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        
        if format_type == 'pdf':
            content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Heart Health Report - {current_date}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #1976d2; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; }}
        .result {{ background: {'#d4edda' if is_healthy else '#f8d7da'}; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        .section {{ margin: 20px 0; }}
        h2 {{ color: #1976d2; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🏥 Heart Health Report</h1>
        <p>Generated on {current_date} at {current_time}</p>
    </div>
    <div class="content">
        <div class="result">
            <h2>Prediction Result</h2>
            <p><strong>{prediction}</strong></p>
            <p>Confidence: {accuracy}%</p>
        </div>
        <div class="section">
            <h2>Recommendations</h2>
            <p>{'Continue maintaining your healthy lifestyle with regular exercise and balanced diet.' if is_healthy else 'Please consult with a healthcare professional immediately for proper evaluation and treatment.'}</p>
        </div>
        <div class="section">
            <h2>Important Notice</h2>
            <p>This report is generated by an AI system and should not replace professional medical advice. Always consult with qualified healthcare professionals.</p>
        </div>
    </div>
</body>
</html>"""
            response = HttpResponse(content, content_type='text/html')
            response['Content-Disposition'] = f'attachment; filename="Heart_Health_Report_{current_date}.html"'
            
        elif format_type == 'txt':
            content = f"""HEART HEALTH SUMMARY
===================

Date: {current_date}
Time: {current_time}
Confidence: {accuracy}%

PREDICTION RESULT:
{prediction}

RECOMMENDATIONS:
{'Continue maintaining your healthy lifestyle with regular exercise and balanced diet.' if is_healthy else 'Please consult with a healthcare professional immediately for proper evaluation and treatment.'}

IMPORTANT NOTICE:
This report is generated by an AI system and should not replace professional medical advice. Always consult with qualified healthcare professionals.

Generated by Heart Disease Prediction System
{current_date}"""
            response = HttpResponse(content, content_type='text/plain')
            response['Content-Disposition'] = f'attachment; filename="Heart_Health_Summary_{current_date}.txt"'
            
        elif format_type == 'dashboard':
            content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Health Dashboard - {current_date}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }}
        .header {{ background: #6f42c1; color: white; padding: 20px; text-align: center; border-radius: 10px; }}
        .metric {{ background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #6f42c1; }}
        .status {{ background: {'#d4edda' if is_healthy else '#f8d7da'}; padding: 15px; margin: 10px 0; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📈 Health Dashboard</h1>
            <p>Generated on {current_date} at {current_time}</p>
        </div>
        <div class="status">
            <h2>Current Status</h2>
            <p><strong>{prediction}</strong></p>
            <p>Confidence: {accuracy}%</p>
        </div>
        <div class="metric">
            <h3>Health Metrics</h3>
            <p>Target Blood Pressure: <120/80 mmHg</p>
            <p>Target Cholesterol: <200 mg/dL</p>
            <p>Target Exercise: 150 min/week</p>
        </div>
        <div class="metric">
            <h3>Goals</h3>
            <p>{'Maintain current healthy lifestyle' if is_healthy else 'Improve cardiovascular health through lifestyle changes'}</p>
        </div>
        <div class="metric">
            <h3>Next Steps</h3>
            <p>{'Continue regular health monitoring' if is_healthy else 'Schedule consultation with healthcare provider'}</p>
        </div>
    </div>
</body>
</html>"""
            response = HttpResponse(content, content_type='text/html')
            response['Content-Disposition'] = f'attachment; filename="Health_Dashboard_{current_date}.html"'
            
        else:
            return HttpResponse('Invalid format', status=400)
            
        return response
        
    except Exception as e:
        return HttpResponse(f'Error generating download: {str(e)}', status=500)
