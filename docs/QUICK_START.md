# 🚀 Quick Start Guide - Run Your Project in 5 Minutes

## Step-by-Step Instructions

### ✅ Step 1: Setup Environment (2 minutes)

**Open Command Prompt/Terminal in project folder:**

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate


# Install dependencies
pip install -r requirements.txt
```

### ✅ Step 2: Setup MySQL Database (1 minute)

**Open MySQL Command Line or MySQL Workbench:**

```sql
CREATE DATABASE Aniket CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**Verify database exists:**
```sql
SHOW DATABASES;
```

### ✅ Step 3: Configure Environment (1 minute)

**Copy environment file:**
```bash
# Windows:
copy env.example .env


**The `.env` file is already configured with:**
- ✅ MySQL database: `Aniket`
- ✅ User: `root`
- ✅ Password: `tiger`
- ✅ Secret key (ready to use)

**If your MySQL credentials are different, edit `.env` file:**
```
DATABASE_NAME=YourDatabaseName
DATABASE_USER=YourUsername
DATABASE_PASSWORD=YourPassword
```

### ✅ Step 4: Run Migrations (30 seconds)

```bash
copy env.example .env
python manage.py migrate
```

### ✅ Step 5: Create Admin User (30 seconds)

```bash
python manage.py createsuperuser
```

**Enter details when prompted:**
- Username: `admin` (or your choice)
- Email: `admin@example.com` (or your choice)
- Password: (enter a strong password)

### ✅ Step 6: Run Server (10 seconds)

```bash
python manage.py runserver
```

### 🎉 You're Done!

**Open your browser and visit:**
- Homepage: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/

**Login with your admin credentials and start using the system!**

---

## 🎨 What You'll See

- **Beautiful animated gradient background**
- **Smooth card animations on hover**
- **Modern glassmorphism effects**
- **Responsive design** (works on mobile too!)

## 🔧 Troubleshooting

### MySQL Connection Error?
1. Make sure MySQL server is running
2. Check database name, username, password in `.env`
3. Verify database exists: `SHOW DATABASES;`

### Migration Errors?
```bash
python manage.py migrate --run-syncdb
```

### Port Already in Use?
Change the port:
```bash
python manage.py runserver 8001
```

---

**Need more details? Check README.md for comprehensive documentation!**

