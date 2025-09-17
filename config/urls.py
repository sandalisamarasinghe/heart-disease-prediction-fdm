from django.contrib import admin
from django.urls import path
from apps.core.health import views as health_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', health_views.Home, name='home'),
    path('login/', health_views.Login_User, name='login'),
    path('guest/predict/', health_views.guest_prediction, name='guest_predict'),
]


