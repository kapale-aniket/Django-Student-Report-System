from django import forms
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
import secrets
import string
from .models import ProjectReport, Feedback, ReportAssignment, EvaluatorStudentAssignment
from accounts.models import User
from django.conf import settings


class ProjectReportForm(forms.ModelForm):
    """Form for submitting project reports"""
    
    class Meta:
        model = ProjectReport
        fields = ['title', 'description', 'department', 'batch', 'supervisor', 'report_file']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'batch': forms.TextInput(attrs={'class': 'form-control'}),
            'supervisor': forms.TextInput(attrs={'class': 'form-control'}),
            'report_file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.docx,.xlsx'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user and self.user.is_student:
            # Pre-fill department and batch for students
            self.fields['department'].initial = self.user.department
            self.fields['batch'].initial = self.user.batch
            self.fields['department'].widget.attrs['readonly'] = True
            self.fields['batch'].widget.attrs['readonly'] = True
    
    def clean_report_file(self):
        """Additional file validation"""
        file = self.cleaned_data.get('report_file')
        if file:
            # Check file extension
            valid_extensions = ['.pdf', '.docx', '.xlsx']
            ext = file.name.split('.')[-1].lower()
            if f'.{ext}' not in valid_extensions:
                raise forms.ValidationError('Only PDF, DOCX, and XLSX files are allowed.')
            
            # Check file size (5MB max)
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError('File size must be less than 5MB.')
        
        return file
    
    def save(self, commit=True):
        """Save form and store original filename"""
        instance = super().save(commit=False)
        if self.cleaned_data.get('report_file'):
            # Store original filename before UUID rename
            original_filename = self.cleaned_data['report_file'].name
            instance._original_filename = original_filename
            instance.original_filename = original_filename
        if commit:
            instance.save()
        return instance


class FeedbackForm(forms.ModelForm):
    """Form for evaluator feedback"""
    
    class Meta:
        model = Feedback
        fields = ['comments', 'grade', 'max_grade']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 6, 'class': 'form-control'}),
            'grade': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'max_grade': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['max_grade'].initial = 100.00


class ReportAssignmentForm(forms.ModelForm):
    """Form for assigning reports to evaluators"""
    
    evaluator = forms.ModelChoiceField(
        queryset=User.objects.filter(role='evaluator'),
        empty_label="Select an evaluator",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = ReportAssignment
        fields = ['evaluator']
    
    def __init__(self, *args, **kwargs):
        self.report = kwargs.pop('report', None)
        super().__init__(*args, **kwargs)
        
        if self.report:
            # Exclude evaluators who are already assigned to this report
            assigned_evaluators = self.report.assignments.filter(is_active=True).values_list('evaluator', flat=True)
            self.fields['evaluator'].queryset = User.objects.filter(role='evaluator').exclude(id__in=assigned_evaluators)


class ReportFilterForm(forms.Form):
    """Form for filtering reports"""
    
    DEPARTMENT_CHOICES = [
        ('', 'All Departments'),
        ('Computer Science', 'Computer Science'),
        ('Information Technology', 'Information Technology'),
        ('Electronics', 'Electronics'),
        ('Mechanical', 'Mechanical'),
        ('Civil', 'Civil'),
        ('Electrical', 'Electrical'),
    ]
    
    STATUS_CHOICES = [
        ('', 'All Statuses'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('evaluated', 'Evaluated'),
        ('rejected', 'Rejected'),
    ]
    
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, required=False, 
                                 widget=forms.Select(attrs={'class': 'form-control'}))
    batch = forms.CharField(max_length=20, required=False, 
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Batch'}))
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False,
                              widget=forms.Select(attrs={'class': 'form-control'}))
    student = forms.CharField(max_length=100, required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student name'}))


class CreateEvaluatorForm(forms.ModelForm):
    """Admin creates evaluator accounts"""
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'department', 'phone_number']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError(f'A user with username "{username}" already exists. Please choose a different username.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Check if email already exists
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError(f'A user with email "{email}" already exists. Please use a different email address.')
        return email

    def save(self, commit=True):
        user: User = super().save(commit=False)
        user.role = 'evaluator'
        user.is_active = True
        password = None
        if commit:
            # Generate secure random password using secrets module
            password = secrets.token_urlsafe(10)  # Use token_urlsafe for better security
            user.set_password(password)
            user.save()
            # Send email after saving user - ALWAYS store password for display
            user._temp_password = password
            if user.email:
                try:
                    from django.urls import reverse
                    site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
                    login_url = f"{site_url}{reverse('accounts:login')}"
                    # Render HTML email template
                    html_message = render_to_string('emails/credentials_template.html', {
                        'username': user.username,
                        'password': password,
                        'role': 'Evaluator',
                        'user_type': 'Evaluator',
                        'first_name': user.first_name or user.username,
                        'login_url': login_url,
                        'year': timezone.now().year,
                    })
                    send_mail(
                        subject='Your Evaluator Account Credentials - Student Report System',
                        message=f"Hello {user.first_name or user.username},\n\nYour evaluator account has been created.\nUsername: {user.username}\nPassword: {password}\n\nPlease log in at {login_url} and change your password.",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        html_message=html_message,
                        fail_silently=False,
                    )
                    user._email_sent = True
                except Exception as e:
                    # Log error but don't fail user creation
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Failed to send email to {user.email}: {str(e)}", exc_info=True)
                    user._email_sent = False
                    user._email_error = str(e)
            else:
                user._email_sent = False
                user._email_error = "No email address provided"
        else:
            # If not committing, generate password for later use
            password = secrets.token_urlsafe(10)
            user._temp_password = password
        return user


class CreateStudentForm(forms.ModelForm):
    """Evaluator creates student accounts"""
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'student_id', 'department', 'batch', 'phone_number']

    def save(self, commit=True):
        user: User = super().save(commit=False)
        user.role = 'student'
        user.is_active = True
        user.approval_status = 'approved'  # Evaluator-created students are auto-approved
        password = None
        if commit:
            # Generate secure random password using secrets module
            password = secrets.token_urlsafe(10)  # Use token_urlsafe for better security
            user.set_password(password)
            user.save()
            # ALWAYS store password for display
            user._temp_password = password
            if user.email:
                try:
                    site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
                    login_url = f"{site_url}{reverse('accounts:login')}"
                    # Render HTML email template
                    html_message = render_to_string('emails/credentials_template.html', {
                        'username': user.username,
                        'password': password,
                        'role': 'Student',
                        'user_type': 'Student',
                        'first_name': user.first_name or user.username,
                        'login_url': login_url,
                        'year': timezone.now().year,
                    })
                    send_mail(
                        subject='Your Student Account Credentials - Student Report System',
                        message=f"Hello {user.first_name or user.username},\n\nYour student account has been created.\nUsername: {user.username}\nPassword: {password}\n\nPlease log in at {login_url} and change your password.",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        html_message=html_message,
                        fail_silently=False,
                    )
                    user._email_sent = True
                except Exception as e:
                    # Log error but don't fail user creation
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Failed to send email to {user.email}: {str(e)}", exc_info=True)
                    user._email_sent = False
                    user._email_error = str(e)
            else:
                user._email_sent = False
                user._email_error = "No email address provided"
        else:
            # If not committing, generate password for later use
            password = secrets.token_urlsafe(10)
            user._temp_password = password
        return user


class AssignStudentsToEvaluatorForm(forms.Form):
    """Admin picks students to assign to an evaluator"""
    evaluator = forms.ModelChoiceField(queryset=User.objects.filter(role='evaluator'), widget=forms.Select(attrs={'class': 'form-control'}))
    students = forms.ModelMultipleChoiceField(queryset=User.objects.filter(role='student'), widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': 12}))


