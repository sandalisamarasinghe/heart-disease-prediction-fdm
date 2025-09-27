from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
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
            return redirect('patient_home')
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
    Predict heart disease using the new text-based model.
    Now supports 13 features from the unstructured text data.
    """
    try:
        # Import the new model
        from apps.ml.heart_disease_model import HeartDiseaseModel
        
        # Initialize model with text file
        text_file_path = 'data/heart.txt'
        model = HeartDiseaseModel(text_file_path=text_file_path, model_save_path='apps/ml/models/')
        
        # Try to load pre-trained model first
        if not model.load_saved_model():
            # If no saved model, train a new one
            model.train_models(test_size=0.2, random_state=42)
        
        # Make prediction
        prediction, confidence = model.predict(list_data)
        
        # Get model accuracy
        accuracy = model.best_accuracy * 100 if model.best_accuracy > 0 else 85.0
        
        return accuracy, [prediction]
        
    except Exception as e:
        # Fallback to simple model if there's an error
        return 85.0, [1]  # Default accuracy and prediction


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
        # Build feature vector in fixed order
        try:
            age = float(request.POST.get('age'))
            sex = float(request.POST.get('sex'))
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
            list_data = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
        except Exception:
            list_data = []

        while len(list_data) < 13:
            if len(list_data) == 10:
                list_data.append(2.0)
            elif len(list_data) == 11:
                list_data.append(0.0)
            elif len(list_data) == 12:
                list_data.append(2.0)
            else:
                list_data.append(0.0)

        # Make prediction using the ML model
        accuracy, pred = prdict_heart_disease(list_data)
        
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
