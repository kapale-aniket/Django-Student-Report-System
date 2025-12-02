# 🎓 Student Report System

A comprehensive **Django-based Project Report Management System** featuring role-based access control, secure file uploads, email automation, and a modern responsive UI.

![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![MySQL](https://img.shields.io/badge/MySQL-5.7+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [API Endpoints](#-api-endpoints)
- [Environment Variables](#-environment-variables)
- [Usage Guide](#-usage-guide)
- [Common Issues](#-common-issues)
- [Contributing](#-contributing)

---

## ✨ Features

### 🔐 Authentication & Authorization
- **Role-Based Access Control**: Admin, Evaluator, and Student roles
- **Secure Login System**: Custom authentication with role-based redirects
- **Session Management**: Secure session handling with automatic logout
- **No Password Reset**: For security, password reset option is disabled

### 📁 File Management
- **Secure File Upload**: UUID-based file naming system
- **Multiple Format Support**: PDF, DOCX, XLSX files
- **File Size Validation**: Maximum 5MB per file
- **Organized Storage**: Files organized by department, batch, and student

### 📧 Email Automation
- **Auto Credentials**: Automatic password generation and email delivery
- **HTML Emails**: Professional, responsive email templates
- **SMTP Integration**: Gmail SMTP support with App Password authentication
- **Error Handling**: Graceful handling of email failures

### 🎨 Modern UI/UX
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern Animations**: AOS (Animate On Scroll) library
- **Gradient Backgrounds**: Beautiful gradient effects
- **Glassmorphism**: Frosted glass effect on cards
- **Bootstrap 5**: Latest Bootstrap framework
- **Font Awesome**: Icon library for better visuals

### 📊 Dashboard Features
- **Role-Specific Dashboards**: Customized dashboards for each role
- **Statistics**: Real-time statistics and metrics
- **Report Filtering**: Advanced filtering by department, batch, status
- **Search Functionality**: Search reports by student name

### 🔒 Security Features
- **CSRF Protection**: Built-in CSRF token validation
- **SQL Injection Prevention**: Django ORM protection
- **XSS Protection**: Auto-escaping in templates
- **File Validation**: Server-side file type and size validation
- **Environment Variables**: Sensitive data stored in `.env` file

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 4.2.7
- **Database**: MySQL 5.7+ / SQLite3 (development)
- **ORM**: Django ORM
- **Authentication**: Django Authentication System

### Frontend
- **CSS Framework**: Bootstrap 5.3.0
- **Icons**: Font Awesome 6.0.0
- **Animations**: AOS (Animate On Scroll) 2.3.1
- **Fonts**: Google Fonts (Poppins)

### Additional Libraries
- **Form Handling**: django-crispy-forms, crispy-bootstrap5
- **Environment Config**: python-decouple
- **Email**: Django SMTP backend
- **Image Processing**: Pillow

### Development Tools
- **Language**: Python 3.8+
- **Package Manager**: pip
- **Virtual Environment**: venv
- **Version Control**: Git

---

## 📸 Screenshots

### Login Page
- Clean, professional login interface
- Role-based authentication
- Student registration option

### Admin Dashboard
- User management
- Report overview
- Statistics and metrics

### Student Dashboard
- Report submission interface
- View submitted reports
- Track evaluation status

### Evaluator Dashboard
- Assigned reports view
- Feedback submission
- Student management

*Note: Screenshots can be added here or linked to a screenshots folder*

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- MySQL Server 5.7+ (or SQLite3 for development)
- pip (Python package manager)
- Git (optional, for cloning)

### Step-by-Step Installation

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd Django-Student-Report-System
```

#### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** If you encounter issues installing `mysqlclient` on Windows:
- Download MySQL Connector C from MySQL website
- Or use PyMySQL as an alternative (already included)

#### 4. Setup Database

**MySQL:**
```sql
CREATE DATABASE Aniket CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**Or use SQLite3** (no setup needed, change in `.env`)

#### 5. Configure Environment Variables

```bash
# Copy example file
cp env.example .env

# Edit .env file with your settings
# See Environment Variables section below
```

#### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 7. Create Admin User

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

#### 8. Run Development Server

```bash
python manage.py runserver
```

Access the application at: **http://127.0.0.1:8000/**

---

## 📁 Project Structure

```
Django-Student-Report-System/
│
├── accounts/                    # User authentication app
│   ├── models.py               # Custom User model with roles
│   ├── views.py                # Login, logout, profile views
│   ├── forms.py                # Registration and password forms
│   ├── urls.py                 # Authentication URLs
│   └── migrations/             # Database migrations
│
├── reports/                     # Main reports application
│   ├── models.py               # ProjectReport, Feedback models
│   ├── views.py                # Dashboard, upload, download views
│   ├── forms.py                # Report submission forms
│   ├── urls.py                 # Report management URLs
│   └── migrations/             # Database migrations
│
├── templates/                   # HTML templates
│   ├── base/                   # Base templates
│   │   └── base.html          # Main layout template
│   ├── accounts/               # Authentication templates
│   │   ├── home.html          # Login page
│   │   ├── login.html         # Alternative login
│   │   └── profile.html       # User profile
│   ├── reports/                # Report management templates
│   │   ├── admin_dashboard.html
│   │   ├── student_dashboard.html
│   │   └── evaluator_dashboard.html
│   ├── emails/                 # Email templates
│   │   └── password_reset_email.html
│   └── errors/                 # Error pages (404, 403, 500)
│
├── static/                      # Static files (CSS, JS, images)
├── media/                       # Uploaded files (auto-generated)
├── logs/                        # Error logs (auto-generated)
│
├── student_report_system/       # Main project settings
│   ├── settings.py             # Django configuration
│   ├── urls.py                 # Root URL configuration
│   ├── wsgi.py                 # WSGI configuration
│   ├── asgi.py                 # ASGI configuration
│   ├── middleware.py           # Custom middleware
│   └── views.py                # Error handlers
│
├── docs/                        # Documentation folder
│   └── [various documentation files]
│
├── .env                         # Environment variables (create from env.example)
├── .gitignore                   # Git ignore rules
├── env.example                  # Example environment file
├── requirements.txt             # Python dependencies
├── manage.py                    # Django management script
├── README.md                    # This file
└── PROJECT_STRUCTURE.md         # Detailed project structure
```

See `PROJECT_STRUCTURE.md` for detailed structure information.

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory (copy from `env.example`):

```env
# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Database Configuration (MySQL)
DATABASE_ENGINE=django.db.backends.mysql
DATABASE_NAME=Aniket
DATABASE_USER=root
DATABASE_PASSWORD=your-password
DATABASE_HOST=localhost
DATABASE_PORT=3306

# Email Configuration (Gmail SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
SITE_URL=http://127.0.0.1:8000
```

### Gmail SMTP Setup

1. Enable **2-Step Verification** in your Google Account
2. Generate **App Password**: 
   - Go to Google Account → Security → App passwords
   - Create app password for "Mail"
   - Use the 16-character password in `.env`
3. **Never use your regular Gmail password!**

---

## 🔌 API Endpoints

### Authentication URLs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home/Login page |
| `/login/` | GET, POST | Login form |
| `/logout/` | GET, POST | Logout user |
| `/profile/` | GET, POST | User profile |
| `/register/` | GET, POST | Student registration |

### Report Management URLs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/reports/admin/` | GET | Admin dashboard |
| `/reports/student/` | GET | Student dashboard |
| `/reports/evaluator/` | GET | Evaluator dashboard |
| `/reports/submit/` | GET, POST | Submit report |
| `/reports/all-reports/` | GET | View all reports |
| `/reports/users/` | GET | User management (Admin) |
| `/reports/users/add-evaluator/` | GET, POST | Add evaluator (Admin) |
| `/reports/students/add/` | GET, POST | Add student (Evaluator) |

---

## 💻 Usage Guide

### For Admin Users

1. **Login** with admin credentials
2. **Create Evaluators**:
   - Go to "Add Evaluator"
   - Enter evaluator details
   - Credentials sent via email automatically
3. **Manage Users**:
   - View all users in "User Management"
   - Assign students to evaluators
   - Delete evaluators if needed
4. **View Reports**:
   - Access all reports in "All Reports"
   - Filter by department, batch, status
   - Download any report

### For Students

1. **Register/Login**:
   - New students can register from home page
   - Wait for evaluator approval
   - Login after approval
2. **Submit Reports**:
   - Click "Submit Report"
   - Fill report details
   - Upload file (PDF, DOCX, XLSX, max 5MB)
3. **View Reports**:
   - Dashboard shows all submitted reports
   - Check evaluation status
   - View feedback from evaluators

### For Evaluators

1. **Login** with evaluator credentials
2. **Review Reports**:
   - View assigned reports
   - Provide feedback and grades
   - Update report status
3. **Manage Students**:
   - Create student accounts
   - Approve/reject student registrations
   - View assigned students

---

## 🐛 Common Issues & Solutions

### Issue 1: MySQL Connection Error

**Error:** `django.db.utils.OperationalError: (2003, "Can't connect to MySQL server")`

**Solution:**
- Ensure MySQL server is running
- Check database credentials in `.env`
- Verify database exists: `CREATE DATABASE Aniket;`

### Issue 2: Migration Errors

**Solution:**
```bash
python manage.py makemigrations
python manage.py migrate --run-syncdb
```

### Issue 3: mysqlclient Installation Failed (Windows)

**Solution:**
```bash
# Option 1: Install MySQL Connector C first
# Option 2: Use PyMySQL (already in requirements.txt)
# Add to manage.py before imports:
import pymysql
pymysql.install_as_MySQLdb()
```

### Issue 4: Static Files Not Loading

**Solution:**
```bash
python manage.py collectstatic
```

### Issue 5: Email Not Sending

**Solution:**
- Check Gmail App Password (not regular password)
- Verify `.env` email settings
- Check SMTP settings are correct
- See `docs/GMAIL_SETUP_GUIDE.md` for detailed instructions

---

## 🔒 Security Notes

- **Never commit `.env` file** to version control
- Use **App Passwords** for Gmail, not regular passwords
- Set `DEBUG=False` in production
- Update `ALLOWED_HOSTS` for production deployment
- Use strong `SECRET_KEY` in production

---

## 📚 Documentation

Additional documentation files are available in the `docs/` folder:
- Feature checklist
- Setup guides
- Troubleshooting guides
- Email configuration guides

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is for educational purposes.

---

## 👨‍💻 Author

**Your Name**
- Email: your.email@example.com
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- GitHub: [@yourusername](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- Django community for excellent documentation
- Bootstrap team for the amazing framework
- Font Awesome for beautiful icons

---

**Built with ❤️ using Django**

**Happy Coding! 🚀**
