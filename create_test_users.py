#!/usr/bin/env python
"""
Script to create specific test users for the Student Report System
Creates: 1 Admin, 1 Evaluator, 1 Student with specific credentials
"""
import os
import sys
import django

# Configure PyMySQL to work with Django (for MySQL connection)
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass  # PyMySQL not installed, use default MySQLdb

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_report_system.settings')
django.setup()

from accounts.models import User
from django.utils import timezone

def create_test_users():
    """Create specific test users with predefined credentials"""
    
    print("=" * 60)
    print("Creating Test Users for Student Report System")
    print("=" * 60)
    
    # Create Admin User
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@studentreport.local',
            'first_name': 'System',
            'last_name': 'Administrator',
            'role': 'admin',
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
            'approval_status': 'approved',
        }
    )
    if created:
        admin.set_password('admin123')
        admin.save()
        print(f"\n✓ Created ADMIN user")
        print(f"  Username: admin")
        print(f"  Password: admin123")
    else:
        admin.set_password('admin123')
        admin.save()
        print(f"\n✓ Updated ADMIN user")
        print(f"  Username: admin")
        print(f"  Password: admin123")
    
    # Create Evaluator User
    evaluator, created = User.objects.get_or_create(
        username='evaluator',
        defaults={
            'email': 'evaluator@studentreport.local',
            'first_name': 'Dr. Sarah',
            'last_name': 'Johnson',
            'role': 'evaluator',
            'department': 'Computer Science',
            'phone_number': '+1-555-0100',
            'is_active': True,
            'approval_status': 'approved',
        }
    )
    if created:
        evaluator.set_password('evaluator123')
        evaluator.save()
        print(f"\n✓ Created EVALUATOR user")
        print(f"  Username: evaluator")
        print(f"  Password: evaluator123")
    else:
        evaluator.set_password('evaluator123')
        evaluator.save()
        print(f"\n✓ Updated EVALUATOR user")
        print(f"  Username: evaluator")
        print(f"  Password: evaluator123")
    
    # Create Student User
    student, created = User.objects.get_or_create(
        username='student',
        defaults={
            'email': 'student@studentreport.local',
            'first_name': 'Alex',
            'last_name': 'Williams',
            'role': 'student',
            'student_id': 'STU2024001',
            'department': 'Computer Science',
            'batch': '2024',
            'phone_number': '+1-555-0101',
            'is_active': True,
            'approval_status': 'approved',  # Pre-approved for immediate access
        }
    )
    if created:
        student.set_password('student123')
        student.save()
        print(f"\n✓ Created STUDENT user")
        print(f"  Username: student")
        print(f"  Password: student123")
    else:
        student.set_password('student123')
        student.approval_status = 'approved'
        student.is_active = True
        student.save()
        print(f"\n✓ Updated STUDENT user")
        print(f"  Username: student")
        print(f"  Password: student123")
    
    print("\n" + "=" * 60)
    print("Test Users Created Successfully!")
    print("=" * 60)
    print("\nCREDENTIALS SUMMARY:")
    print("-" * 60)
    print(f"Admin:")
    print(f"  Username: admin")
    print(f"  Password: admin123")
    print(f"  Role: Administrator (Full System Access)")
    print("\nEvaluator:")
    print(f"  Username: evaluator")
    print(f"  Password: evaluator123")
    print(f"  Role: Evaluator (Can approve students, evaluate reports)")
    print("\nStudent:")
    print(f"  Username: student")
    print(f"  Password: student123")
    print(f"  Role: Student (Can submit reports)")
    print("\n" + "=" * 60)
    print("\nYou can now login to the system using these credentials.")
    print("Start the server with: python manage.py runserver")
    print("=" * 60)
    
    return admin, evaluator, student

if __name__ == '__main__':
    try:
        create_test_users()
    except Exception as e:
        print(f"\n❌ Error creating test users: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)







