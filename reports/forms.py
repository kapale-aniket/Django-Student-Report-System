from django import forms
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import ProjectReport, Feedback, ReportAssignment, EvaluatorStudentAssignment
from accounts.models import User


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

    def save(self, commit=True):
        user: User = super().save(commit=False)
        user.role = 'evaluator'
        user.is_active = True
        if commit:
            password = get_random_string(length=10)
            user.set_password(password)
            user.save()
            if user.email:
                send_mail(
                    subject='Your Evaluator Account Credentials',
                    message=f"Hello {user.first_name or user.username},\n\nYour evaluator account has been created.\nUsername: {user.username}\nPassword: {password}\n\nPlease log in and change your password.",
                    from_email=None,
                    recipient_list=[user.email],
                    fail_silently=True,
                )
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
        if commit:
            password = get_random_string(length=10)
            user.set_password(password)
            user.save()
            if user.email:
                send_mail(
                    subject='Your Student Account Credentials',
                    message=f"Hello {user.first_name or user.username},\n\nYour student account has been created.\nUsername: {user.username}\nPassword: {password}\n\nPlease log in and change your password.",
                    from_email=None,
                    recipient_list=[user.email],
                    fail_silently=True,
                )
        return user


class AssignStudentsToEvaluatorForm(forms.Form):
    """Admin picks students to assign to an evaluator"""
    evaluator = forms.ModelChoiceField(queryset=User.objects.filter(role='evaluator'), widget=forms.Select(attrs={'class': 'form-control'}))
    students = forms.ModelMultipleChoiceField(queryset=User.objects.filter(role='student'), widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': 12}))


