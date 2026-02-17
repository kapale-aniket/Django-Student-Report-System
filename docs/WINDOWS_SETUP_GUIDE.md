# 🪟 Windows Setup Guide - Easy Installation

## ✅ Quick Fix for Installation Issues

If you encountered errors installing `mysqlclient` or `Pillow`, here's the easy solution:

### Problem:
- `mysqlclient` requires Visual C++ Build Tools (difficult to install on Windows)
- Old `Pillow` versions may not have pre-built wheels

### Solution:
We use **PyMySQL** instead of `mysqlclient` - it's pure Python and works on Windows without any compilers!

---

## 📦 Installation Steps

### Step 1: Install Core Packages

```powershell
# Install Django and basic packages (no compilation needed)
pip install Django==4.2.7 python-decouple django-crispy-forms crispy-bootstrap5

# Install PyMySQL (pure Python, no compiler needed)
pip install PyMySQL

# Install Pillow (will use pre-built wheel)
pip install Pillow
```

### Step 2: Verify Installation

```powershell
python manage.py --version
```

You should see: `4.2.7`

---

## ✅ Already Done!

The `manage.py` file has been updated to automatically configure PyMySQL. You don't need to do anything else!

---

## 🚀 Now Run Your Project

```powershell
# 1. Make sure MySQL database exists
# Run in MySQL: CREATE DATABASE Aniket;

# 2. Run migrations
python manage.py makemigrations
python manage.py migrate

# 3. Create admin user
python manage.py createsuperuser

# 4. Run server
python manage.py runserver
```

---

## 📝 Updated requirements.txt

The `requirements.txt` has been updated to use:
- ✅ `PyMySQL` instead of `mysqlclient`
- ✅ Flexible Pillow version (uses pre-built wheels)

---

## 🔧 Troubleshooting

### If PyMySQL is not found:

Make sure it's installed in your virtual environment:

```powershell
pip install PyMySQL
```

### If MySQL connection fails:

1. Check MySQL server is running
2. Verify database exists: `SHOW DATABASES;`
3. Check `.env` file has correct MySQL credentials

---

**You're all set! No C++ compiler needed! 🎉**


