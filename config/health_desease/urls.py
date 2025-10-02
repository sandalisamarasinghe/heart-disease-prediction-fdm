"""health_desease URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.health.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home, name="home"),
    path('home/', Home, name="home_alt"),
    path('user_home/', User_Home,name="user_home"),
    path('admin_home/', Admin_Home,name="admin_home"),
    path('about/', About,name="about"),
    path('contact/', Contact,name="contact"),
    path('gallery/', Gallery,name="gallery"),
    path('login/', Login_User,name="login"),
    path('login_admin/', Login_admin,name="login_admin"),
    path('signup/', Signup_User,name="signup"),
    path('logout/', Logout,name="logout"),
    path('change_password/', Change_Password,name="change_password"),
    # path('prdict_heart_disease', prdict_heart_disease,name="prdict_heart_disease"),
    path('add_heartdetail/', add_heartdetail,name="add_heartdetail"),
    # Guest prediction (no login required)
    path('guest_prediction/', guest_prediction,name="guest_prediction"),
    # Alias route so buttons can point to prediction_form
    path('prediction_form/', guest_prediction,name="prediction_form"),
    # Enhanced prediction with all 16 features
    # guest prediction disabled
    path('view_search_pat/', view_search_pat,name="view_search_pat"),
    path('api/latest_predictions/', get_latest_predictions,name="get_latest_predictions"),

    path('view_feedback/', View_Feedback,name="view_feedback"),
    path('edit_profile/', Edit_My_deatail,name="edit_profile"),
    path('profile_doctor/', View_My_Detail,name="profile_doctor"),
    path('sent_feedback/', sent_feedback,name="sent_feedback"),

    path('delete_searched/<int:pid>/', delete_searched, name="delete_searched"),
    path('delete_feedback/<int:pid>/', delete_feedback, name="delete_feedback"),
    path('predict_desease/<str:pred>/<str:accuracy>/', predict_desease, name="predict_desease"),
    # Download URLs
    path('download/<str:format_type>/', download_report, name="download_report"),
    # Model Status URL
    path('model_status/', model_status, name="model_status"),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
