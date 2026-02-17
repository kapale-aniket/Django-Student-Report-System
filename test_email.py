"""
Test Email Configuration Script
Run this to verify your Gmail SMTP settings are correct.
"""
import os
import sys

# Setup PyMySQL before Django
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_report_system.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email_configuration():
    """Test if email configuration is working"""
    print("=" * 60)
    print("EMAIL CONFIGURATION TEST")
    print("=" * 60)
    print()
    
    # Display current configuration
    print("Current Email Settings:")
    print(f"  EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"  EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'NOT SET'}")
    print(f"  DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print()
    
    # Check if password is set
    if not settings.EMAIL_HOST_PASSWORD:
        print("❌ ERROR: EMAIL_HOST_PASSWORD is not set in .env file!")
        print()
        return False
    
    # Check if password looks like a regular password (might be wrong)
    password = settings.EMAIL_HOST_PASSWORD
    if len(password) < 16 and '@' in password:
        print("⚠️  WARNING: Your password looks like a regular Gmail password.")
        print("   Gmail requires an App Password (16 characters, no special chars like @)")
        print("   See GMAIL_SETUP_GUIDE.md for instructions")
        print()
    
    # Ask for test email
    test_email = input("Enter your email address to send a test email (or press Enter to skip): ").strip()
    
    if not test_email:
        print("Skipping email test.")
        return True
    
    print()
    print("Attempting to send test email...")
    print()
    
    try:
        send_mail(
            subject='Test Email - Student Report System',
            message='This is a test email from your Django application. If you receive this, your email configuration is working correctly!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[test_email],
            fail_silently=False,
        )
        print("✅ SUCCESS! Test email sent successfully!")
        print(f"   Check your inbox at: {test_email}")
        print()
        return True
    except Exception as e:
        print("❌ ERROR: Failed to send email!")
        print(f"   Error: {str(e)}")
        print()
        
        # Provide specific guidance based on error
        error_str = str(e)
        if '535' in error_str or 'BadCredentials' in error_str:
            print("🔧 SOLUTION:")
            print("   This is a Gmail authentication error.")
            print("   You need to use a Gmail App Password, not your regular password.")
            print()
            print("   Steps to fix:")
            print("   1. Enable 2-Step Verification: https://myaccount.google.com/security")
            print("   2. Generate App Password: https://myaccount.google.com/apppasswords")
            print("   3. Update .env file: EMAIL_HOST_PASSWORD=your_16_char_app_password")
            print("   4. Restart Django server")
            print()
            print("   See GMAIL_SETUP_GUIDE.md for detailed instructions")
        elif 'Connection' in error_str or 'timeout' in error_str.lower():
            print("🔧 SOLUTION:")
            print("   Connection issue. Check:")
            print("   - Internet connection")
            print("   - Firewall settings")
            print("   - EMAIL_HOST and EMAIL_PORT in .env")
        else:
            print("🔧 SOLUTION:")
            print("   Check your .env file configuration")
            print("   See GMAIL_SETUP_GUIDE.md for help")
        
        print()
        return False

if __name__ == '__main__':
    try:
        success = test_email_configuration()
        if success:
            print("=" * 60)
            print("Email configuration test completed.")
            print("=" * 60)
        else:
            print("=" * 60)
            print("Email configuration needs to be fixed.")
            print("=" * 60)
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

