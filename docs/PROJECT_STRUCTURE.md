# 📁 Project Structure

## 🏗️ **Standard Django Project Organization**

This project follows Django best practices with a clean, modular structure:

```
Heart-Disease-Prediction-System/
├── 📁 apps/                          # Application modules
│   ├── 📁 core/                      # Core application
│   │   └── 📁 health/                # Main Django app
│   │       ├── 📁 migrations/        # Database migrations
│   │       ├── 📁 static/            # Static files (CSS, JS, images)
│   │       ├── 📁 templates/         # HTML templates
│   │       ├── __init__.py
│   │       ├── admin.py              # Admin interface
│   │       ├── api_views.py          # API views
│   │       ├── apps.py               # App configuration
│   │       ├── choices.py            # Model choices
│   │       ├── forms.py              # Django forms
│   │       ├── models.py             # Database models
│   │       ├── serializers.py        # API serializers
│   │       ├── tests.py              # Unit tests
│   │       └── views.py              # View functions
│   ├── 📁 api/                       # API applications (future)
│   └── 📁 ml/                        # Machine Learning
│       └── 📁 Machine_Learning/      # ML models and data
│           └── new_heart_dataset.csv # 10-feature dataset
├── 📁 config/                        # Configuration files
│   ├── 📁 health_desease/            # Django project settings
│   │   ├── __init__.py
│   │   ├── api.py                    # API configuration
│   │   ├── apirep.py                 # API reports
│   │   ├── asgi.py                   # ASGI configuration
│   │   ├── routing.py                # WebSocket routing
│   │   ├── settings.py               # Django settings
│   │   ├── urls.py                   # URL configuration
│   │   ├── urls1.py                  # Additional URLs
│   │   └── wsgi.py                   # WSGI configuration
│   ├── .gitattributes               # Git configuration
│   └── settings.py                   # Main settings file
├── 📁 docs/                          # Documentation
│   ├── README.md                     # Project overview
│   ├── CLEANUP_SUMMARY.md           # Cleanup documentation
│   └── PROJECT_STRUCTURE.md         # This file
├── 📁 media/                         # User uploaded files
├── 📁 scripts/                       # Utility scripts
├── .gitignore                        # Git ignore rules
├── manage.py                         # Django management script
├── requirements.txt                  # Python dependencies
└── db.sqlite3                        # SQLite database
```

## 🎯 **Directory Purposes**

### **📁 apps/**
Contains all application modules organized by functionality:

- **core/**: Main application logic
- **api/**: API-specific applications (future expansion)
- **ml/**: Machine learning models and data

### **📁 config/**
Configuration and settings files:

- **health_desease/**: Original Django project settings
- **settings.py**: Main settings file that imports from Django project
- **.gitattributes**: Git configuration

### **📁 docs/**
Project documentation:

- **README.md**: Project overview and setup instructions
- **CLEANUP_SUMMARY.md**: Documentation of system cleanup
- **PROJECT_STRUCTURE.md**: This structure documentation

### **📁 media/**
User-uploaded files and media content

### **📁 scripts/**
Utility scripts for deployment, maintenance, etc.

## 🔧 **Key Files**

### **Configuration Files**
- `manage.py`: Django management script
- `config/settings.py`: Main Django settings
- `requirements.txt`: Python dependencies
- `.gitignore`: Git ignore patterns

### **Application Files**
- `apps/core/health/views.py`: Main application logic
- `apps/core/health/models.py`: Database models
- `apps/core/health/admin.py`: Admin interface
- `apps/ml/Machine_Learning/new_heart_dataset.csv`: ML dataset

### **Static Files**
- `apps/core/health/static/css/modern-style.css`: Main stylesheet
- `apps/core/health/static/css/bootstrap.css`: Bootstrap framework
- `apps/core/health/static/css/font-awesome.min.css`: Icon styles

## 🚀 **Benefits of This Structure**

### **Modularity**
- ✅ **Separation of Concerns**: Each app has a specific purpose
- ✅ **Scalability**: Easy to add new applications
- ✅ **Maintainability**: Clear organization makes maintenance easier

### **Standards Compliance**
- ✅ **Django Best Practices**: Follows Django conventions
- ✅ **Python Standards**: Adheres to PEP 8 and Python best practices
- ✅ **Professional Structure**: Industry-standard organization

### **Development Workflow**
- ✅ **Clear Navigation**: Easy to find files and understand structure
- ✅ **Team Collaboration**: Standard structure for team development
- ✅ **Deployment Ready**: Organized for production deployment

## 📋 **File Naming Conventions**

### **Python Files**
- Use lowercase with underscores: `views.py`, `models.py`
- Descriptive names: `heart_disease_prediction.py`
- Follow PEP 8 naming conventions

### **Template Files**
- Use lowercase with underscores: `add_heartdetail.html`
- Descriptive names: `patient_dashboard.html`
- Group related templates in subdirectories

### **Static Files**
- Use lowercase with hyphens: `modern-style.css`
- Descriptive names: `heart-disease-icons.svg`
- Organize by type: `css/`, `js/`, `images/`

### **Configuration Files**
- Use descriptive names: `production_settings.py`
- Follow Django conventions: `urls.py`, `settings.py`
- Use environment-specific suffixes: `settings_dev.py`

## 🔄 **Migration from Old Structure**

The project has been reorganized from the original structure:

### **Before (Original)**
```
Heart-Disease-Prediction-System-main/
├── health/                          # Django app
├── health_desease/                  # Django project
├── Machine_Learning/                # ML files
├── README.md                        # Documentation
└── manage.py                        # Management script
```

### **After (Standard)**
```
Heart-Disease-Prediction-System/
├── apps/core/health/                # Django app
├── config/health_desease/           # Django project
├── apps/ml/Machine_Learning/        # ML files
├── docs/README.md                   # Documentation
└── manage.py                        # Management script
```

## 🎯 **Next Steps**

1. **Update Import Paths**: Ensure all imports work with new structure
2. **Test Functionality**: Verify all features work correctly
3. **Update Documentation**: Keep documentation current
4. **Add Tests**: Implement comprehensive testing
5. **Deploy**: Prepare for production deployment

---

**📁 This structure provides a clean, professional, and scalable foundation for the Heart Disease Prediction System!**

