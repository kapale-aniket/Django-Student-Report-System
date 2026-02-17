from django.core.management.base import BaseCommand
from accounts.models import User
from reports.models import ProjectReport, ReportAssignment
import os


class Command(BaseCommand):
    help = 'Create demo users and sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating demo users and data...')
        
        try:
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
            self.stdout.write(self.style.SUCCESS('✓ Created demo student: student1' if created else '✓ Updated demo student: student1'))
            
            # Verify student can authenticate
            if not student.check_password('demo123'):
                self.stdout.write(self.style.ERROR('ERROR: Student password verification failed!'))
                return

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
                    'is_active': True
                }
            )
            evaluator.set_password('demo123')
            evaluator.is_active = True
            evaluator.save()
            self.stdout.write(self.style.SUCCESS('✓ Created demo evaluator: evaluator1' if created else '✓ Updated demo evaluator: evaluator1'))
            
            # Verify evaluator can authenticate
            if not evaluator.check_password('demo123'):
                self.stdout.write(self.style.ERROR('ERROR: Evaluator password verification failed!'))
                return

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
                    'is_active': True
                }
            )
            admin.set_password('demo123')
            admin.is_staff = True
            admin.is_superuser = True
            admin.is_active = True
            admin.save()
            self.stdout.write(self.style.SUCCESS('✓ Created demo admin: admin1' if created else '✓ Updated demo admin: admin1'))
            
            # Verify admin can authenticate
            if not admin.check_password('demo123'):
                self.stdout.write(self.style.ERROR('ERROR: Admin password verification failed!'))
                return
            
            # Final verification - try to authenticate all users
            from django.contrib.auth import authenticate
            test_admin = authenticate(username='admin1', password='demo123')
            test_evaluator = authenticate(username='evaluator1', password='demo123')
            test_student = authenticate(username='student1', password='demo123')
            
            if not all([test_admin, test_evaluator, test_student]):
                self.stdout.write(self.style.WARNING('WARNING: Some users failed authentication test'))
                if not test_admin:
                    self.stdout.write(self.style.ERROR('  - admin1 authentication failed'))
                if not test_evaluator:
                    self.stdout.write(self.style.ERROR('  - evaluator1 authentication failed'))
                if not test_student:
                    self.stdout.write(self.style.ERROR('  - student1 authentication failed'))
            else:
                self.stdout.write(self.style.SUCCESS('✓ All users can authenticate successfully'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'ERROR creating demo users: {str(e)}'))
            import traceback
            self.stdout.write(traceback.format_exc())
            raise
        
            # Create sample report file (optional, skip if fails)
            try:
                media_dir = 'media/reports/Computer Science/2024'
                os.makedirs(media_dir, exist_ok=True)
                
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
                    self.stdout.write(self.style.SUCCESS('✓ Created demo report: Web Development Project'))
                    
                    # Assign evaluator to report
                    assignment, created = ReportAssignment.objects.get_or_create(
                        report=report,
                        evaluator=evaluator,
                        defaults={
                            'assigned_by': admin,
                            'is_active': True
                        }
                    )
                    
                    if created:
                        self.stdout.write(self.style.SUCCESS('✓ Assigned evaluator to report'))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Note: Could not create demo report data: {str(e)}'))
            
            self.stdout.write(self.style.SUCCESS('\n✓ Demo users created successfully!'))
            self.stdout.write('\n' + '='*60)
            self.stdout.write('DEMO CREDENTIALS (ready to use):')
            self.stdout.write('='*60)
            self.stdout.write('Student:   student1   / demo123')
            self.stdout.write('Evaluator: evaluator1 / demo123') 
            self.stdout.write('Admin:     admin1     / demo123')
            self.stdout.write('='*60 + '\n')
