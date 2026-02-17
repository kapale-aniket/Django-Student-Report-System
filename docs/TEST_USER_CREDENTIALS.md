# Test User Credentials

This file contains the credentials for the test users created for the Student Report System.

## User Accounts

### Administrator Account
- **Username:** `admin`
- **Password:** `admin123`
- **Role:** Administrator
- **Email:** admin@studentreport.local
- **Access:** Full system access, can create evaluators, manage users

### Evaluator Account
- **Username:** `evaluator`
- **Password:** `evaluator123`
- **Role:** Evaluator
- **Email:** evaluator@studentreport.local
- **Access:** Can approve/reject student registrations, evaluate reports

### Student Account
- **Username:** `student`
- **Password:** `student123`
- **Role:** Student
- **Email:** student@studentreport.local
- **Student ID:** STU2024001
- **Access:** Can submit reports (pre-approved)

## Creating Test Users

To create these test users, run the following command:

```bash
python create_test_users.py
```

This script will create or update the three test users with the credentials listed above.

## Notes

- All passwords are simple for testing purposes. Change them in production.
- The student account is pre-approved and active for immediate access.
- The evaluator account can approve pending student registrations.
- The admin account has full system privileges.

## Security Warning

⚠️ **DO NOT USE THESE CREDENTIALS IN PRODUCTION!**

These are test credentials with weak passwords intended only for development and testing purposes.

