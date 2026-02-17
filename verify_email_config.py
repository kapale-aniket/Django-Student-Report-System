"""
Quick Email Configuration Verifier
Run this to check if your .env email settings are correct.
"""
import os
import re

def check_env_file():
    """Check .env file for email configuration"""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    if not os.path.exists(env_path):
        print("❌ ERROR: .env file not found!")
        print(f"   Expected at: {env_path}")
        return False
    
    print("=" * 60)
    print("CHECKING .env FILE EMAIL CONFIGURATION")
    print("=" * 60)
    print()
    
    with open(env_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract email settings
    email_user = None
    email_password = None
    
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('EMAIL_HOST_USER='):
            email_user = line.split('=', 1)[1].strip()
        elif line.startswith('EMAIL_HOST_PASSWORD='):
            email_password = line.split('=', 1)[1].strip()
    
    print("Current Configuration:")
    print(f"  EMAIL_HOST_USER: {email_user or 'NOT SET'}")
    
    if email_password:
        # Check if it looks like a regular password (has @ or is short)
        if '@' in email_password:
            print(f"  EMAIL_HOST_PASSWORD: {email_password[:3]}*** (HIDDEN)")
            print()
            print("❌ PROBLEM DETECTED!")
            print("   Your password contains '@' which means it's a regular password.")
            print("   Gmail requires an App Password (16 characters, no @ symbol).")
            print()
            print("🔧 FIX REQUIRED:")
            print("   1. Go to: https://myaccount.google.com/apppasswords")
            print("   2. Generate a 16-character App Password")
            print("   3. Replace the password in .env file")
            print("   4. Restart Django server")
            print()
            return False
        elif len(email_password) < 16:
            print(f"  EMAIL_HOST_PASSWORD: {email_password[:3]}*** (HIDDEN)")
            print()
            print("⚠️  WARNING:")
            print(f"   Your password is only {len(email_password)} characters.")
            print("   Gmail App Passwords are typically 16 characters.")
            print("   Make sure you're using an App Password, not a regular password.")
            print()
            return False
        else:
            print(f"  EMAIL_HOST_PASSWORD: {email_password[:3]}*** (HIDDEN - {len(email_password)} chars)")
            print()
            print("✅ Password format looks correct!")
            print("   (16+ characters, no @ symbol)")
            print()
            print("If you're still getting errors:")
            print("  1. Make sure 2-Step Verification is enabled")
            print("  2. Make sure you're using the App Password (not regular password)")
            print("  3. Restart Django server after updating .env")
            print()
            return True
    else:
        print("  EMAIL_HOST_PASSWORD: NOT SET")
        print()
        print("❌ ERROR: EMAIL_HOST_PASSWORD is not set in .env file!")
        return False

if __name__ == '__main__':
    try:
        result = check_env_file()
        print("=" * 60)
        if result:
            print("✅ Configuration check passed!")
            print("   If emails still fail, check Gmail App Password setup.")
        else:
            print("❌ Configuration needs to be fixed!")
            print("   See FIX_THIS_NOW.md for instructions.")
        print("=" * 60)
    except Exception as e:
        print(f"❌ Error checking configuration: {str(e)}")
        import traceback
        traceback.print_exc()



