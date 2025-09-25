"""
Django Settings Configuration
Main settings file that imports from the Django project settings
"""

import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Add apps directory to Python path
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Import Django project settings
from config.health_desease.settings import *

# Override settings for production if needed
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'apps', 'core', 'health', 'static'),
]

# Media files configuration (renamed folder -> data)
MEDIA_URL = '/data/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'data')

# Templates configuration
TEMPLATES[0]['DIRS'] = [
    os.path.join(BASE_DIR, 'apps', 'core', 'health', 'templates'),
]

# Update INSTALLED_APPS to use correct path
if 'health' in INSTALLED_APPS:
    INSTALLED_APPS.remove('health')
INSTALLED_APPS.append('core.health')

# Update ROOT_URLCONF to use correct path
ROOT_URLCONF = 'config.health_desease.urls'

# Update WSGI_APPLICATION to use correct path
WSGI_APPLICATION = 'config.health_desease.wsgi.application'

# CSRF trusted origins for local development
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
]
