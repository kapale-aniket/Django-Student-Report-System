from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from .models import User


class StudentRegistrationForm(UserCreationForm):
    """Form for student self-registration (requires evaluator approval)"""
    
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    student_id = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Student ID'}))
    department = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Computer Science'}))
    batch = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2024'}))
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'student_id', 
                 'department', 'batch', 'phone_number', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.role = 'student'
        user.student_id = self.cleaned_data['student_id']
        user.department = self.cleaned_data['department']
        user.batch = self.cleaned_data['batch']
        user.phone_number = self.cleaned_data.get('phone_number', '')
        
        # Set approval status to pending for self-registered students
        user.approval_status = 'pending'
        user.is_active = False  # Inactive until approved
        
        if commit:
            user.save()
            # Send registration confirmation email
            if user.email:
                try:
                    from django.core.mail import send_mail
                    from django.template.loader import render_to_string
                    from django.urls import reverse
                    from django.conf import settings
                    from django.utils import timezone
                    
                    login_url = f"{getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')}{reverse('accounts:login')}"
                    html_message = render_to_string('emails/registration_confirmation.html', {
                        'username': user.username,
                        'first_name': user.first_name or user.username,
                        'login_url': login_url,
                        'year': timezone.now().year,
                    })
                    send_mail(
                        subject='Student Account Registration - Pending Approval',
                        message=f"Hello {user.first_name or user.username},\n\nThank you for registering as a student.\nUsername: {user.username}\n\nYour account is pending approval from an evaluator. You will receive another email once your account is approved and activated.",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        html_message=html_message,
                        fail_silently=False,
                    )
                except Exception as e:
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Failed to send registration email to {user.email}: {str(e)}")
        return user


class UserRegistrationForm(UserCreationForm):
    """Form for user registration with role selection (for admin)"""
    
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    student_id = forms.CharField(max_length=20, required=False, help_text="Required for students")
    department = forms.CharField(max_length=100, required=False)
    batch = forms.CharField(max_length=20, required=False)
    phone_number = forms.CharField(max_length=15, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 
                 'student_id', 'department', 'batch', 'phone_number', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student_id'].required = False
        self.fields['department'].required = False
        self.fields['batch'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        student_id = cleaned_data.get('student_id')
        
        if role == 'student' and not student_id:
            raise forms.ValidationError("Student ID is required for students.")
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.role = self.cleaned_data['role']
        user.student_id = self.cleaned_data['student_id']
        user.department = self.cleaned_data['department']
        user.batch = self.cleaned_data['batch']
        user.phone_number = self.cleaned_data['phone_number']
        
        # Admin-created users are automatically approved
        if user.role == 'student':
            user.approval_status = 'approved'
        
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """Form for updating user profile"""
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'student_id', 
                 'department', 'batch', 'phone_number']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.role != 'student':
            self.fields['student_id'].widget.attrs['readonly'] = True


class CustomPasswordResetForm(PasswordResetForm):
    """Custom password reset form that only allows students and evaluators"""
    
    def get_users(self, email):
        """Get users by email, but only students and evaluators"""
        active_users = User.objects.filter(
            email__iexact=email,
            is_active=True
        )
        # Only allow password reset for students and evaluators
        return active_users.filter(role__in=['student', 'evaluator'])


class CustomSetPasswordForm(SetPasswordForm):
    """Custom set password form with Bootstrap styling"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to password fields
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your new password',
            'autofocus': True
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your new password'
        })
