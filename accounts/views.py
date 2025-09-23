from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserRegistrationForm, UserUpdateForm
from .models import User


class CustomLoginView(LoginView):
    """Custom login view - redirect to appropriate dashboard"""
    template_name = 'accounts/login.html'
    
    def get_success_url(self):
        """Redirect to appropriate dashboard based on user role"""
        user = self.request.user
        if user.is_admin:
            return reverse_lazy('reports:admin_dashboard')
        elif user.is_student:
            return reverse_lazy('reports:student_dashboard')
        elif user.is_evaluator:
            return reverse_lazy('reports:evaluator_dashboard')
        else:
            return reverse_lazy('accounts:home')


class CustomLogoutView(LogoutView):
    """Custom logout view"""
    next_page = reverse_lazy('accounts:home')


class UserRegistrationView(CreateView):
    """User registration view"""
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registration successful! You can now log in using the credentials above.')
        return response


@login_required
def profile_view(request):
    """User profile view"""
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user,
    }
    return render(request, 'accounts/profile.html', context)


def home_view(request):
    """Home page view - handle login form submission"""
    if request.method == 'POST':
        # Handle login form submission
        username = request.POST.get('username')
        password = request.POST.get('password')
        _selected_role = request.POST.get('selected_role')  # not enforced, used only for UX hints
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to appropriate dashboard
                if user.is_student:
                    return redirect('reports:student_dashboard')
                elif user.is_evaluator:
                    return redirect('reports:evaluator_dashboard')
                elif user.is_admin:
                    return redirect('reports:admin_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    return render(request, 'accounts/home.html')