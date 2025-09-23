from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    """Form for user registration with role selection"""
    
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

