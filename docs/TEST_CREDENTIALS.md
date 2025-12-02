# 🔐 Test Credentials Guide

## 🎯 How to Create Test Users

This guide explains how to create test users for development and testing purposes.

---

## 👨‍🎓 Creating Test Students

### Option 1: Via Evaluator Dashboard
1. Login as Evaluator
2. Go to "Add Student"
3. Fill in student details
4. System generates random password
5. Credentials sent via email

### Option 2: Via Django Admin
1. Login to `/admin/`
2. Go to Accounts → Users
3. Add new user
4. Set role to "Student"
5. Set password manually

---

## 👨‍🏫 Creating Test Evaluators

### Via Admin Dashboard
1. Login as Admin
2. Go to "Add Evaluator"
3. Fill in evaluator details
4. System generates random password
5. Credentials sent via email

---

## 👨‍💼 Creating Admin User

### Via Command Line
```bash
python manage.py createsuperuser
```

### Via Django Admin
1. Login to `/admin/`
2. Go to Accounts → Users
3. Add new user
4. Set role to "Admin"
5. Make superuser and staff

---

## 🧪 Recommended Test Data

### Student Test User:
- Username: `student_test`
- Email: `student@test.com`
- Role: Student
- Department: Computer Science
- Batch: 2024

### Evaluator Test User:
- Username: `evaluator_test`
- Email: `evaluator@test.com`
- Role: Evaluator
- Department: Computer Science

### Admin Test User:
- Username: `admin_test`
- Email: `admin@test.com`
- Role: Admin

---

## 🔒 Security Notes

- **For Development**: Use simple passwords like `demo123`
- **For Production**: Always use strong, unique passwords
- **Never commit real passwords** to version control
- **Use environment variables** for sensitive data

---

## 📝 Note

This is a guide for creating test users. Actual credentials should not be stored in documentation or version control.
