#!/usr/bin/env python
"""
Script to create default admin account for the Student Report System
This script should be run once to set up the initial admin account
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
import secrets

def create_default_admin():
    """Create default admin account with secure password"""
    
    print("=" * 70)
    print("Creating Default Admin Account for Student Report System")
    print("=" * 70)
    
    # Generate secure random password
    admin_password = secrets.token_urlsafe(12)  # 12 characters, URL-safe
    
    # Check if admin already exists
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
        admin.set_password(admin_password)
        admin.save()
        print(f"\n✓ Default ADMIN account created successfully!")
    else:
        # Update existing admin password
        admin.set_password(admin_password)
        admin.email = 'admin@studentreport.local'
        admin.first_name = 'System'
        admin.last_name = 'Administrator'
        admin.role = 'admin'
        admin.is_staff = True
        admin.is_superuser = True
        admin.is_active = True
        admin.approval_status = 'approved'
        admin.save()
        print(f"\n✓ Default ADMIN account updated successfully!")
    
    print("\n" + "=" * 70)
    print("DEFAULT ADMIN CREDENTIALS")
    print("=" * 70)
    print(f"\n⚠️  IMPORTANT: Save these credentials securely!")
    print(f"\nUsername: admin")
    print(f"Password: {admin_password}")
    print(f"\n" + "=" * 70)
    print("\nSecurity Notes:")
    print("- This password is randomly generated and secure")
    print("- Please change the password after first login")
    print("- Do not share these credentials publicly")
    print("- Store them in a secure password manager")
    print("\n" + "=" * 70)
    
    # Save to file for user
    credentials_file = 'ADMIN_CREDENTIALS.txt'
    with open(credentials_file, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("DEFAULT ADMIN CREDENTIALS - STUDENT REPORT SYSTEM\n")
        f.write("=" * 70 + "\n\n")
        f.write("⚠️  IMPORTANT: Save these credentials securely!\n\n")
        f.write(f"Username: admin\n")
        f.write(f"Password: {admin_password}\n\n")
        f.write("=" * 70 + "\n")
        f.write("Security Notes:\n")
        f.write("- This password is randomly generated and secure\n")
        f.write("- Please change the password after first login\n")
        f.write("- Do not share these credentials publicly\n")
        f.write("- Store them in a secure password manager\n")
        f.write("\n" + "=" * 70 + "\n")
    
    print(f"\n✓ Credentials have been saved to: {credentials_file}")
    print("=" * 70 + "\n")
    
    return admin, admin_password

if __name__ == '__main__':
    try:
        admin, password = create_default_admin()
        print("Default admin account setup complete!")
    except Exception as e:
        print(f"\n❌ Error creating default admin: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

