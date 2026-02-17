from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Extended User model with role-based access"""
    
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('evaluator', 'Evaluator'),
        ('admin', 'Admin'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    student_id = models.CharField(max_length=20, blank=True, null=True, unique=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    batch = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    # Approval status for self-registered students
    APPROVAL_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    approval_status = models.CharField(max_length=20, choices=APPROVAL_CHOICES, default='approved', 
                                      help_text='For students: pending approval from evaluator')
    approved_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='approved_students',
                                   help_text='Evaluator who approved this student')
    approval_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_student(self):
        return self.role == 'student'
    
    @property
    def is_evaluator(self):
        return self.role == 'evaluator'
    
    @property
    def is_admin(self):
        return self.role == 'admin' or getattr(self, 'is_superuser', False)