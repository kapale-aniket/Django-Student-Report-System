#!/usr/bin/env python
"""
Quick script to update EMAIL_HOST_PASSWORD in .env file
Usage: python update_email_password.py
"""
import os
import re

def update_email_password():
    env_file = '.env'
    
    if not os.path.exists(env_file):
        print(f"❌ Error: {env_file} file not found!")
        return False
    
    print("=" * 60)
    print("UPDATE EMAIL PASSWORD IN .env FILE")
    print("=" * 60)
    print()
    print("Current .env file location:", os.path.abspath(env_file))
    print()
    
    # Read current content
    with open(env_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find current password
    match = re.search(r'EMAIL_HOST_PASSWORD=(.+)', content)
    if match:
        current_password = match.group(1).strip()
        if len(current_password) >= 6:
            masked = current_password[:3] + "*" * (len(current_password) - 6) + current_password[-3:]
        else:
            masked = "*" * len(current_password)
        print(f"Current password: {masked} ({len(current_password)} characters)")
    else:
        print("Current password: NOT FOUND")
    
    print()
    print("Enter your Gmail App Password (16 characters, alphanumeric only):")
    print("(Or press Enter to cancel)")
    new_password = input("> ").strip()
    
    if not new_password:
        print("\nCancelled.")
        return False
    
    # Remove spaces if user pasted with spaces
    new_password = new_password.replace(' ', '')
    
    # Validate format
    if len(new_password) != 16:
        print(f"\n⚠️  Warning: Password is {len(new_password)} characters (should be 16)")
        confirm = input("Continue anyway? (y/n): ").strip().lower()
        if confirm != 'y':
            return False
    
    if not new_password.isalnum():
        print("\n⚠️  Warning: Password contains special characters")
        print("Gmail App Passwords are usually alphanumeric only")
        confirm = input("Continue anyway? (y/n): ").strip().lower()
        if confirm != 'y':
            return False
    
    # Update the file
    pattern = r'EMAIL_HOST_PASSWORD=.+'
    replacement = f'EMAIL_HOST_PASSWORD={new_password}'
    
    if re.search(pattern, content):
        updated_content = re.sub(pattern, replacement, content)
    else:
        # Add if not found
        updated_content = content + f'\nEMAIL_HOST_PASSWORD={new_password}\n'
    
    # Write back
    try:
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print()
        print("=" * 60)
        print("✅ SUCCESS! Password updated in .env file")
        print("=" * 60)
        print()
        print("Next steps:")
        print("  1. Restart your Django server (Ctrl+C, then python manage.py runserver)")
        print("  2. Test email: python test_email_now.py")
        print("  3. Or create an evaluator to test")
        print()
        return True
    except Exception as e:
        print(f"\n❌ Error updating file: {e}")
        return False

if __name__ == '__main__':
    update_email_password()


