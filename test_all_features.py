#!/usr/bin/env python
"""
Comprehensive Test Script - Verify All Features Work
Tests all URLs, views, and functionality
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_report_system.settings')
django.setup()

from django.urls import reverse, NoReverseMatch
from django.test import Client
from django.contrib.auth import get_user_model
from accounts.models import User

User = get_user_model()

def test_url_patterns():
    """Test all URL patterns exist and are accessible"""
    print("=" * 60)
    print("TESTING ALL URL PATTERNS")
    print("=" * 60)
    print()
    
    urls_to_test = [
        # Accounts URLs
        ('accounts:home', None, 'Home Page'),
        ('accounts:login', None, 'Login Page'),
        ('accounts:logout', None, 'Logout'),
        ('accounts:profile', None, 'Profile'),
        ('accounts:student_register', None, 'Student Registration'),
        ('accounts:password_reset', None, 'Password Reset'),
        
        # Reports URLs - Student
        ('reports:student_dashboard', None, 'Student Dashboard'),
        ('reports:submit_report', None, 'Submit Report'),
        
        # Reports URLs - Evaluator
        ('reports:evaluator_dashboard', None, 'Evaluator Dashboard'),
        ('reports:evaluator_view_students', None, 'Evaluator View Students'),
        ('reports:evaluator_add_student', None, 'Evaluator Add Student'),
        ('reports:pending_students', None, 'Pending Students'),
        ('reports:all_reports', None, 'All Reports'),
        
        # Reports URLs - Admin
        ('reports:admin_dashboard', None, 'Admin Dashboard'),
        ('reports:user_management', None, 'User Management'),
        ('reports:admin_add_evaluator', None, 'Admin Add Evaluator'),
        ('reports:admin_assign_students', None, 'Admin Assign Students'),
    ]
    
    passed = 0
    failed = 0
    
    for url_name, args, description in urls_to_test:
        try:
            if args:
                url = reverse(url_name, args=args)
            else:
                url = reverse(url_name)
            print(f"✅ {description:30} -> {url}")
            passed += 1
        except NoReverseMatch as e:
            print(f"❌ {description:30} -> ERROR: {str(e)}")
            failed += 1
        except Exception as e:
            print(f"❌ {description:30} -> ERROR: {str(e)}")
            failed += 1
    
    print()
    print(f"Results: {passed} passed, {failed} failed")
    return failed == 0


def test_home_page():
    """Test home page loads correctly"""
    print()
    print("=" * 60)
    print("TESTING HOME PAGE")
    print("=" * 60)
    print()
    
    client = Client()
    
    try:
        # Test unauthenticated access
        response = client.get('/')
        if response.status_code == 200:
            print("✅ Home page loads correctly (200 OK)")
            
            # Check if login form is present
            if 'form' in response.context or 'login' in response.content.decode().lower():
                print("✅ Login form is present")
            else:
                print("⚠️  Warning: Login form may not be visible")
            
            return True
        else:
            print(f"❌ Home page returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error accessing home page: {str(e)}")
        return False


def test_authentication_required():
    """Test that protected pages require authentication"""
    print()
    print("=" * 60)
    print("TESTING AUTHENTICATION REQUIREMENTS")
    print("=" * 60)
    print()
    
    client = Client()
    protected_urls = [
        ('/reports/student/', 'Student Dashboard'),
        ('/reports/evaluator/', 'Evaluator Dashboard'),
        ('/reports/admin/', 'Admin Dashboard'),
        ('/accounts/profile/', 'Profile'),
    ]
    
    all_passed = True
    for url, name in protected_urls:
        try:
            response = client.get(url)
            if response.status_code in [302, 403]:  # Redirect to login or forbidden
                print(f"✅ {name:30} -> Requires authentication (redirected/forbidden)")
            else:
                print(f"⚠️  {name:30} -> Status: {response.status_code} (may allow unauthenticated access)")
                all_passed = False
        except Exception as e:
            print(f"❌ {name:30} -> Error: {str(e)}")
            all_passed = False
    
    return all_passed


def test_user_roles():
    """Test that users exist for each role"""
    print()
    print("=" * 60)
    print("TESTING USER ROLES")
    print("=" * 60)
    print()
    
    try:
        admin_count = User.objects.filter(role='admin').count()
        evaluator_count = User.objects.filter(role='evaluator').count()
        student_count = User.objects.filter(role='student').count()
        
        print(f"Admin users:     {admin_count}")
        print(f"Evaluator users: {evaluator_count}")
        print(f"Student users:   {student_count}")
        
        if admin_count > 0:
            print("✅ Admin users exist")
        else:
            print("⚠️  Warning: No admin users found")
        
        if evaluator_count > 0:
            print("✅ Evaluator users exist")
        else:
            print("⚠️  Warning: No evaluator users found")
        
        if student_count > 0:
            print("✅ Student users exist")
        else:
            print("⚠️  Warning: No student users found")
        
        return True
    except Exception as e:
        print(f"❌ Error checking user roles: {str(e)}")
        return False


def test_cache_headers():
    """Test that no-cache headers are set"""
    print()
    print("=" * 60)
    print("TESTING CACHE HEADERS")
    print("=" * 60)
    print()
    
    client = Client()
    
    try:
        response = client.get('/')
        cache_control = response.get('Cache-Control', '')
        pragma = response.get('Pragma', '')
        
        if 'no-cache' in cache_control.lower():
            print("✅ Cache-Control header set correctly")
        else:
            print(f"⚠️  Cache-Control header: {cache_control or 'Not set'}")
        
        if pragma:
            print(f"✅ Pragma header: {pragma}")
        else:
            print("⚠️  Pragma header not set")
        
        return 'no-cache' in cache_control.lower()
    except Exception as e:
        print(f"❌ Error checking cache headers: {str(e)}")
        return False


def main():
    """Run all tests"""
    print()
    print("=" * 60)
    print("COMPREHENSIVE FEATURE TEST")
    print("Student Report System")
    print("=" * 60)
    print()
    
    results = []
    
    # Run all tests
    results.append(("URL Patterns", test_url_patterns()))
    results.append(("Home Page", test_home_page()))
    results.append(("Authentication", test_authentication_required()))
    results.append(("User Roles", test_user_roles()))
    results.append(("Cache Headers", test_cache_headers()))
    
    # Summary
    print()
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print()
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    print()
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("⚠️  Some tests failed. Review the output above.")
    
    print()
    print("=" * 60)
    print()


if __name__ == '__main__':
    main()


