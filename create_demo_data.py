#!/usr/bin/env python
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
from reports.models import ProjectReport, ReportAssignment

def create_demo_users():
    """Create demo users for testing"""
    
    # Create demo student (always set password so login works after re-run)
    student, created = User.objects.get_or_create(
        username='student1',
        defaults={
            'email': 'student1@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'student',
            'student_id': 'STU001',
            'department': 'Computer Science',
            'batch': '2024',
            'phone_number': '1234567890',
            'is_active': True,
            'approval_status': 'approved',
        }
    )
    student.set_password('demo123')
    student.is_active = True
    student.approval_status = 'approved'
    student.save()
    print("Created demo student: student1" if created else "Updated demo student: student1")

    # Create demo evaluator
    evaluator, created = User.objects.get_or_create(
        username='evaluator1',
        defaults={
            'email': 'evaluator1@example.com',
            'first_name': 'Dr. Jane',
            'last_name': 'Smith',
            'role': 'evaluator',
            'department': 'Computer Science',
            'phone_number': '0987654321',
            'is_active': True,
        }
    )
    evaluator.set_password('demo123')
    evaluator.is_active = True
    evaluator.save()
    print("Created demo evaluator: evaluator1" if created else "Updated demo evaluator: evaluator1")

    # Create demo admin
    admin, created = User.objects.get_or_create(
        username='admin1',
        defaults={
            'email': 'admin1@example.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'role': 'admin',
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
        }
    )
    admin.set_password('demo123')
    admin.is_staff = True
    admin.is_superuser = True
    admin.is_active = True
    admin.save()
    print("Created demo admin: admin1" if created else "Updated demo admin: admin1")
    
    return student, evaluator, admin

def create_demo_reports(student):
    """Create demo project reports"""
    
    # Create a sample report file
    import tempfile
    import os
    
    # Create media directory if it doesn't exist
    media_dir = 'media/reports/Computer Science/2024'
    os.makedirs(media_dir, exist_ok=True)
    
    # Create a dummy report file
    report_file_path = os.path.join(media_dir, 'sample_report.txt')
    with open(report_file_path, 'w') as f:
        f.write("This is a sample project report for demonstration purposes.\n")
        f.write("It contains information about a student project.\n")
        f.write("The report demonstrates the file upload functionality.\n")
    
    # Create demo report
    report, created = ProjectReport.objects.get_or_create(
        title='Web Development Project',
        student=student,
        defaults={
            'description': 'A comprehensive web development project using Django and React',
            'department': 'Computer Science',
            'batch': '2024',
            'supervisor': 'Dr. Jane Smith',
            'report_file': 'reports/Computer Science/2024/sample_report.txt',
            'status': 'submitted'
        }
    )
    
    if created:
        print("Created demo report: Web Development Project")
    
    return report

if __name__ == '__main__':
    print("Creating demo data...")
    
    # Create demo users
    student, evaluator, admin = create_demo_users()
    
    # Create demo report
    report = create_demo_reports(student)
    
    print("\nDemo data created successfully!")
    print("\nDemo accounts:")
    print("Student: student1 / demo123")
    print("Evaluator: evaluator1 / demo123") 
    print("Admin: admin1 / demo123")
    print("\nYou can now start the server with: python manage.py runserver")
