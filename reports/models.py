from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import os
import uuid

User = get_user_model()


def validate_file_size(value):
    """Validate file size - max 5MB"""
    max_size = 5 * 1024 * 1024  # 5MB in bytes
    if value.size > max_size:
        raise ValidationError(f'File size must be less than 5MB. Current size: {value.size / (1024 * 1024):.2f}MB')


def upload_to_reports(instance, filename):
    """Generate upload path with UUID-based unique filename"""
    # Get file extension
    ext = filename.split('.')[-1]
    # Generate UUID filename
    uuid_filename = f"{uuid.uuid4()}.{ext}"
    # Store original filename in uuid_name field will be handled in save method
    return f'reports/{uuid_filename}'


class ProjectReport(models.Model):
    """Model for storing project reports"""
    
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('evaluated', 'Evaluated'),
        ('rejected', 'Rejected'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_reports')
    department = models.CharField(max_length=100)
    batch = models.CharField(max_length=20)
    supervisor = models.CharField(max_length=100, blank=True, null=True)
    report_file = models.FileField(
        upload_to=upload_to_reports,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'xlsx']),
            validate_file_size
        ],
        help_text="Upload PDF, DOCX, or XLSX files only (Max size: 5MB)"
    )
    uuid_name = models.CharField(max_length=255, blank=True, help_text="Unique UUID-based filename")
    original_filename = models.CharField(max_length=255, blank=True, help_text="Original filename uploaded by user")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        """Override save to set uuid_name from filename"""
        if self.report_file:
            if not self.uuid_name:
                # Extract UUID filename from report_file name
                self.uuid_name = os.path.basename(self.report_file.name)
            # Store original filename if provided
            if hasattr(self, '_original_filename') and self._original_filename and not self.original_filename:
                self.original_filename = self._original_filename
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Project Report'
        verbose_name_plural = 'Project Reports'
    
    def __str__(self):
        return f"{self.title} - {self.student.username}"
    
    @property
    def filename(self):
        """Return the original filename for display"""
        return self.original_filename or os.path.basename(self.report_file.name) if self.report_file else None
    
    @property
    def stored_filename(self):
        """Return the UUID-based stored filename"""
        return self.uuid_name or (os.path.basename(self.report_file.name) if self.report_file else None)
    
    @property
    def file_size(self):
        try:
            return f"{self.report_file.size / 1024:.1f} KB"
        except:
            return "Unknown"


class Feedback(models.Model):
    """Model for storing evaluator feedback on reports"""
    
    report = models.ForeignKey(ProjectReport, on_delete=models.CASCADE, related_name='feedbacks')
    evaluator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_feedbacks')
    comments = models.TextField()
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    max_grade = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['report', 'evaluator']
    
    def __str__(self):
        return f"Feedback for {self.report.title} by {self.evaluator.username}"
    
    @property
    def grade_percentage(self):
        if self.grade and self.max_grade:
            return (self.grade / self.max_grade) * 100
        return 0


class ReportAssignment(models.Model):
    """Model for assigning reports to evaluators"""
    
    report = models.ForeignKey(ProjectReport, on_delete=models.CASCADE, related_name='assignments')
    evaluator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_reports')
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_reports_admin')
    assigned_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['report', 'evaluator']
        ordering = ['-assigned_at']
    
    def __str__(self):
        return f"{self.report.title} assigned to {self.evaluator.username}"


class EvaluatorStudentAssignment(models.Model):
    """Mapping of evaluator to students they are allowed to evaluate"""
    evaluator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evaluator_student_mappings')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_evaluator_mappings')
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='admin_mapped_students')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['evaluator', 'student']
        verbose_name = 'Evaluator-Student Assignment'
        verbose_name_plural = 'Evaluator-Student Assignments'

    def __str__(self):
        return f"{self.student.username} -> {self.evaluator.username}"