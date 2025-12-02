# 📁 Project Structure Documentation

This document provides a detailed overview of the Student Report System project structure.

---

## 🗂️ Root Directory Structure

```
Django-Student-Report-System/
│
├── 📁 accounts/                 # User Authentication Application
├── 📁 reports/                  # Report Management Application
├── 📁 templates/                # HTML Templates
├── 📁 static/                   # Static Files (CSS, JS, Images)
├── 📁 media/                    # Uploaded Files (Auto-generated)
├── 📁 logs/                     # Error Logs (Auto-generated)
├── 📁 docs/                     # Documentation Files
├── 📁 student_report_system/    # Main Project Settings
│
├── 📄 .env                      # Environment Variables (Not in Git)
├── 📄 .gitignore                # Git Ignore Rules
├── 📄 env.example               # Example Environment File
├── 📄 requirements.txt          # Python Dependencies
├── 📄 manage.py                 # Django Management Script
├── 📄 README.md                 # Main Project Documentation
└── 📄 PROJECT_STRUCTURE.md      # This File
```

---

## 📦 Applications Structure

### 1. **accounts/** - Authentication App

```
accounts/
├── __init__.py
├── admin.py                  # Admin configuration
├── apps.py                   # App configuration
├── forms.py                  # User registration & login forms
├── models.py                 # Custom User model
├── urls.py                   # URL routing
├── views.py                  # Authentication views
├── tests.py                  # Unit tests
│
├── 📁 migrations/            # Database migrations
│   ├── __init__.py
│   ├── 0001_initial.py
│   └── 0002_user_approval_date_user_approval_status_and_more.py
│
└── 📁 management/            # Custom management commands
    └── commands/
        └── create_demo_users.py
```

**Key Files:**
- `models.py`: Custom User model with roles (Admin, Evaluator, Student)
- `views.py`: Login, logout, profile, password reset views
- `forms.py`: User registration, password reset forms

---

### 2. **reports/** - Report Management App

```
reports/
├── __init__.py
├── admin.py                  # Admin configuration
├── apps.py                   # App configuration
├── forms.py                  # Report submission forms
├── models.py                 # Report & Feedback models
├── urls.py                   # URL routing
├── views.py                  # Dashboard & report views
├── tests.py                  # Unit tests
│
└── 📁 migrations/            # Database migrations
    ├── __init__.py
    ├── 0001_initial.py
    ├── 0002_evaluatorstudentassignment.py
    ├── 0003_projectreport_uuid_name.py
    └── 0004_alter_projectreport_report_file.py
```

**Key Files:**
- `models.py`: ProjectReport, Feedback, ReportAssignment models
- `views.py`: Dashboard views for all roles, report upload/download
- `forms.py`: Report submission, feedback, user creation forms

---

## 🎨 Templates Structure

```
templates/
│
├── 📁 base/                  # Base Templates
│   └── base.html            # Main layout template (navbar, sidebar)
│
├── 📁 accounts/              # Authentication Templates
│   ├── home.html            # Home/Login page
│   ├── login.html           # Alternative login page
│   ├── profile.html         # User profile page
│   ├── register.html        # Registration page
│   ├── student_register.html # Student registration
│   ├── password_reset.html   # Password reset request
│   ├── password_reset_confirm.html # Password reset form
│   ├── password_reset_done.html    # Password reset sent
│   └── password_reset_complete.html # Password reset complete
│
├── 📁 reports/               # Report Management Templates
│   ├── admin_dashboard.html      # Admin dashboard
│   ├── student_dashboard.html    # Student dashboard
│   ├── evaluator_dashboard.html  # Evaluator dashboard
│   ├── submit_report.html        # Report submission form
│   ├── all_reports.html          # All reports view
│   ├── report_detail.html        # Report details
│   ├── user_management.html      # User management (Admin)
│   ├── admin_add_evaluator.html  # Add evaluator form
│   ├── evaluator_add_student.html # Add student form
│   ├── evaluator_view_students.html # View assigned students
│   ├── pending_students.html     # Pending approvals
│   └── admin_assign_students.html # Assign students
│
├── 📁 emails/                # Email Templates
│   ├── credentials_template.html      # User credentials email
│   ├── password_reset_email.html      # Password reset email
│   ├── password_reset_subject.txt     # Password reset subject
│   ├── registration_confirmation.html # Registration confirmation
│   └── student_approved.html          # Student approval email
│
└── 📁 errors/                # Error Pages
    ├── 403.html              # Forbidden error
    ├── 404.html              # Not found error
    └── 500.html              # Server error
```

---

## ⚙️ Project Settings Structure

```
student_report_system/
├── __init__.py
├── settings.py              # Main Django settings
├── urls.py                  # Root URL configuration
├── wsgi.py                  # WSGI configuration
├── asgi.py                  # ASGI configuration
├── middleware.py            # Custom middleware (NoCacheMiddleware)
└── views.py                 # Error handlers (404, 403, 500)
```

**Key Settings:**
- Database configuration (MySQL/SQLite)
- Email backend configuration
- Static files configuration
- Installed apps
- Middleware configuration
- Security settings

---

## 📂 Media & Static Files

### Media Files (User Uploads)
```
media/
└── reports/                 # Uploaded report files
    ├── [UUID].pdf          # Files organized by UUID
    └── [Department]/       # Or by department/batch
        └── [Batch]/
            └── [filename]
```

### Static Files
```
static/
├── css/                    # Custom CSS files
├── js/                     # Custom JavaScript files
└── images/                 # Static images
```

---

## 📚 Documentation Folder

```
docs/
├── FEATURE_CHECKLIST.md
├── SETUP_COMPLETE.md
├── GMAIL_SETUP_GUIDE.md
├── QUICK_START_GUIDE.md
├── WINDOWS_SETUP_GUIDE.md
├── CACHE_FIX_COMPLETE.md
├── PASSWORD_RESET_FIX_COMPLETE.md
└── [Other documentation files]
```

---

## 🔑 Key Configuration Files

### `.env` File (Not in Git)
Contains sensitive configuration:
- Database credentials
- Email SMTP settings
- Django secret key
- Debug mode

### `.gitignore`
Excludes from version control:
- `.env` file
- `__pycache__/` directories
- `venv/` virtual environment
- `db.sqlite3` database
- `media/` uploaded files
- `logs/` log files

### `requirements.txt`
Python package dependencies:
- Django==4.2.7
- PyMySQL>=1.1.0
- Pillow>=10.0.0
- python-decouple==3.8
- django-crispy-forms>=2.1
- crispy-bootstrap5>=0.7

---

## 🗄️ Database Models

### User Model (accounts/models.py)
- Extended Django User model
- Roles: Admin, Evaluator, Student
- Approval status for students
- Additional fields: student_id, department, batch

### ProjectReport Model (reports/models.py)
- Report file with UUID naming
- Student reference
- Submission date
- Status tracking
- Original filename preservation

### Feedback Model (reports/models.py)
- Evaluator feedback
- Grades/ratings
- Comments
- Feedback date

---

## 🔗 URL Routing

### Root URLs (student_report_system/urls.py)
- `/` → accounts.urls
- `/reports/` → reports.urls
- `/admin/` → Django admin

### Accounts URLs (accounts/urls.py)
- `/` → Home/Login page
- `/login/` → Login view
- `/logout/` → Logout view
- `/profile/` → User profile
- `/register/` → Student registration
- `/password-reset/` → Password reset

### Reports URLs (reports/urls.py)
- `/reports/admin/` → Admin dashboard
- `/reports/student/` → Student dashboard
- `/reports/evaluator/` → Evaluator dashboard
- `/reports/submit/` → Submit report
- `/reports/all-reports/` → All reports view

---

## 🛡️ Security Features

- **CSRF Protection**: Enabled in all forms
- **Authentication**: Django authentication system
- **Authorization**: Role-based access control
- **File Validation**: Server-side validation
- **SQL Injection Prevention**: Django ORM
- **XSS Protection**: Template auto-escaping
- **Environment Variables**: Sensitive data in `.env`

---

## 📊 File Organization Principles

1. **Separation of Concerns**: Apps separated by functionality
2. **Template Organization**: Templates organized by app and purpose
3. **Static Assets**: Static files in dedicated directory
4. **User Uploads**: Media files in separate directory
5. **Documentation**: All docs in `docs/` folder
6. **Configuration**: Settings in `student_report_system/`

---

**This structure ensures maintainability, scalability, and follows Django best practices.**

