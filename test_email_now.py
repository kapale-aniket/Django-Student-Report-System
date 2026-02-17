#!/usr/bin/env python
"""
Quick Email Test Script
Tests if Gmail SMTP is working with current .env configuration
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_report_system.settings')
django.setup()

from django.conf import settings
from django.core.mail import send_mail
from decouple import config

print("=" * 60)
print("EMAIL CONFIGURATION TEST")
print("=" * 60)
print()

# Display current configuration
email_user = config('EMAIL_HOST_USER', default='')
email_password = config('EMAIL_HOST_PASSWORD', default='')
email_host = config('EMAIL_HOST', default='smtp.gmail.com')
email_port = config('EMAIL_PORT', default=587, cast=int)

print("Current Configuration:")
print(f"  Email: {email_user}")
if email_password:
    # Show first 3 and last 3 characters
    if len(email_password) >= 6:
        masked = email_password[:3] + "*" * (len(email_password) - 6) + email_password[-3:]
    else:
        masked = "*" * len(email_password)
    print(f"  Password: {masked} ({len(email_password)} characters)")
else:
    print(f"  Password: NOT SET")
print(f"  Host: {email_host}")
print(f"  Port: {email_port}")
print()

# Check password format
if email_password:
    if len(email_password) == 16 and email_password.isalnum():
        print("✅ Password format looks correct (16 alphanumeric characters)")
    elif len(email_password) < 16:
        print("⚠️  Password is less than 16 characters (App Passwords are 16 chars)")
    elif not email_password.isalnum():
        print("⚠️  Password contains special characters (App Passwords are alphanumeric only)")
    else:
        print("⚠️  Password format may not be correct")
else:
    print("❌ Password is not set in .env file")
    sys.exit(1)

print()
print("-" * 60)
print()

# Ask for test email
test_email = input("Enter email address to send test email (or press Enter to skip): ").strip()

if not test_email:
    print("\nSkipping email test.")
    print("\nTo test email sending:")
    print("  1. Create an evaluator from Admin Dashboard")
    print("  2. Check if email is received")
    sys.exit(0)

print()
print("Attempting to send test email...")
print()

try:
    send_mail(
        subject='✅ Test Email - Student Report System',
        message='This is a test email from your Django application. If you receive this, your email configuration is working correctly!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[test_email],
        fail_silently=False,
    )
    print("=" * 60)
    print("✅ SUCCESS! Test email sent successfully!")
    print(f"   Check your inbox at: {test_email}")
    print("=" * 60)
    print()
    print("🎉 Your email configuration is working correctly!")
    print("   You can now create evaluators and students - emails will be sent automatically.")
    print()
    
except Exception as e:
    error_str = str(e)
    print("=" * 60)
    print("❌ ERROR: Failed to send email!")
    print("=" * 60)
    print()
    print(f"Error Details: {error_str}")
    print()
    
    # Provide specific guidance
    if '535' in error_str or 'BadCredentials' in error_str or 'Username and Password not accepted' in error_str:
        print("🔍 DIAGNOSIS: Gmail Authentication Failed")
        print()
        print("This means:")
        print("  ❌ Your password is NOT a Gmail App Password")
        print("  ❌ OR 2-Step Verification is not enabled")
        print("  ❌ OR the App Password is incorrect")
        print()
        print("✅ SOLUTION:")
        print("  1. Enable 2-Step Verification: https://myaccount.google.com/security")
        print("  2. Generate App Password: https://myaccount.google.com/apppasswords")
        print("  3. Update .env file with the 16-character App Password")
        print("  4. Restart Django server")
        print("  5. Run this test again")
        print()
        print("📖 See FIX_EMAIL_IMMEDIATELY.md for detailed instructions")
    elif '534' in error_str or 'Application-specific password' in error_str:
        print("🔍 DIAGNOSIS: Need App Password")
        print()
        print("Gmail requires an App Password (not regular password)")
        print("Generate one at: https://myaccount.google.com/apppasswords")
    elif 'Connection' in error_str or 'timeout' in error_str.lower():
        print("🔍 DIAGNOSIS: Connection Issue")
        print()
        print("Check your internet connection and firewall settings")
    else:
        print("🔍 DIAGNOSIS: Unknown Error")
        print()
        print("Check your .env file configuration and try again")
    
    print()
    sys.exit(1)


