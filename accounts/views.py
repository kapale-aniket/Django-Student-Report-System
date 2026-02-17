from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import (
    LoginView, PasswordResetView, PasswordResetDoneView, 
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.utils import timezone
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache
from django.utils.cache import add_never_cache_headers
import logging
from .forms import (
    StudentRegistrationForm, UserRegistrationForm, UserUpdateForm,
    CustomPasswordResetForm, CustomSetPasswordForm
)
from .models import User

logger = logging.getLogger(__name__)


class CustomLoginView(LoginView):
    """Custom login view - redirect to appropriate dashboard"""
    template_name = 'accounts/login.html'
    
    def form_valid(self, form):
        """Check approval status before logging in"""
        user = form.get_user()
        
        # Check if student account is approved
        if user.is_student and user.approval_status != 'approved':
            if user.approval_status == 'pending':
                messages.warning(self.request, 'Your account is pending approval from an evaluator. Please wait for approval.')
            elif user.approval_status == 'rejected':
                messages.error(self.request, 'Your registration has been rejected. Please contact an administrator.')
            return self.form_invalid(form)
        
        # Check if user is active
        if not user.is_active:
            messages.error(self.request, 'Your account is inactive. Please contact an administrator.')
            return self.form_invalid(form)
        
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirect to appropriate dashboard based on user role - NEVER to home"""
        user = self.request.user
        if user.is_admin:
            return reverse_lazy('reports:admin_dashboard')
        elif user.is_student:
            return reverse_lazy('reports:student_dashboard')
        elif user.is_evaluator:
            return reverse_lazy('reports:evaluator_dashboard')
        else:
            # If no role match, redirect to login (not home)
            return reverse_lazy('accounts:login')


@require_http_methods(["GET", "POST"])
@never_cache
def logout_view(request):
    """Custom logout view - properly logs out ALL users (admin, evaluator, student) and redirects to home page"""
    if request.user.is_authenticated:
        # Store user info before logout (since logout clears request.user)
        username = request.user.username
        user_role = request.user.role
        
        # Perform logout - this clears the session and authentication
        logout(request)
        
        # Explicitly flush session to ensure complete cleanup
        request.session.flush()
        
        # Log the logout action
        logger.info(f"User '{username}' (role: {user_role}) logged out successfully")
        
        # Show success message - messages work even after logout due to session framework
        messages.success(request, f'You have been logged out successfully. Goodbye, {username}!')
    
    # Create redirect response with no-cache headers
    response = HttpResponseRedirect(reverse('accounts:home'))
    
    # Add comprehensive no-cache headers to prevent browser caching
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    # Clear session cookie explicitly
    response.delete_cookie('sessionid', path='/')
    response.delete_cookie('csrftoken', path='/')
    
    return response


class StudentRegistrationView(CreateView):
    """Student self-registration view - requires evaluator approval"""
    model = User
    form_class = StudentRegistrationForm
    template_name = 'accounts/student_register.html'
    success_url = reverse_lazy('accounts:home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.info(self.request, 'Registration submitted successfully! Your account is pending approval from an evaluator. You will be notified via email once approved.')
        return response


class UserRegistrationView(CreateView):
    """User registration view (for admin use)"""
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:home')
    
    @login_required
    def dispatch(self, *args, **kwargs):
        """Only allow admins to access this view"""
        if not self.request.user.is_admin:
            return HttpResponseForbidden("Only administrators can access this page.")
        return super().dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'User registered successfully!')
        return response


# Password Reset Views
class CustomPasswordResetView(PasswordResetView):
    """Custom password reset view for students and evaluators"""
    form_class = CustomPasswordResetForm
    template_name = 'accounts/password_reset.html'
    email_template_name = 'emails/password_reset_email.html'
    html_email_template_name = 'emails/password_reset_email.html'  # Ensure HTML email is sent
    subject_template_name = 'emails/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')
    
    def form_valid(self, form):
        messages.info(self.request, 'If an account exists with that email address, you will receive password reset instructions.')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        """Override to use SITE_URL setting for better domain handling"""
        context = super().get_context_data(**kwargs)
        # Use SITE_URL from settings for consistent URL generation
        from django.conf import settings
        site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
        # Parse the URL to get protocol and domain
        from urllib.parse import urlparse
        parsed = urlparse(site_url)
        context['protocol'] = parsed.scheme or 'http'
        context['domain'] = parsed.netloc or '127.0.0.1:8000'
        return context
    
    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None, **kwargs):
        """Override to ensure HTML email is sent with proper content type"""
        from django.template.loader import render_to_string
        from django.utils.html import strip_tags
        from django.conf import settings
        
        # Ensure we use SITE_URL for domain if not already set
        if 'domain' not in context or context.get('domain') == 'example.com':
            site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
            from urllib.parse import urlparse
            parsed = urlparse(site_url)
            context['protocol'] = parsed.scheme or 'http'
            context['domain'] = parsed.netloc or '127.0.0.1:8000'
        
        subject = render_to_string(subject_template_name, context).strip()
        # Remove any newlines from subject
        subject = ' '.join(subject.splitlines())
        
        # Render HTML email
        html_message = render_to_string(email_template_name, context)
        
        # Send HTML email
        send_mail(
            subject=subject,
            message=strip_tags(html_message),  # Plain text fallback
            from_email=from_email,
            recipient_list=[to_email],
            html_message=html_message,  # HTML version
            fail_silently=False,
        )


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """Password reset done view"""
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Password reset confirm view"""
    template_name = 'accounts/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('accounts:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """Password reset complete view"""
    template_name = 'accounts/password_reset_complete.html'


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


@never_cache
def home_view(request):
    """Home page view - ONLY shows login form, NEVER dashboard content"""
    # CRITICAL: Force clear all sessions/cookies to prevent stale redirects
    # This ensures home page ALWAYS shows login form, not cached dashboards
    from django.contrib.sessions.models import Session
    import time
    
    # ALWAYS clear session cookie on home page - start fresh
    # This prevents stale cookies from causing redirects to dashboards
    session_key = request.COOKIES.get('sessionid')
    if session_key:
        try:
            Session.objects.filter(session_key=session_key).delete()
        except:
            pass
    
    # CRITICAL FIX: Only redirect if user is VALIDLY authenticated
    # Check authentication with database validation
    if request.user.is_authenticated:
        try:
            # Force database check - refresh user from database
            user = request.user
            user.refresh_from_db()  # Refresh from database to validate
            
            # Only redirect if user exists, is active, and has valid session
            if user.is_active and hasattr(user, 'role'):
                if user.is_admin:
                    return redirect('reports:admin_dashboard')
                elif user.is_student:
                    return redirect('reports:student_dashboard')
                elif user.is_evaluator:
                    return redirect('reports:evaluator_dashboard')
        except Exception as e:
            # User doesn't exist or session is invalid - clear everything
            from django.contrib.auth import logout
            logout(request)
            request.session.flush()
            logger.warning(f"Cleared invalid session on home page: {e}")
    
    # At this point, we're showing login page - ensure clean state
    # Don't delete cookies here as they may be needed for CSRF
    
    # Handle login form submission on home page (ONLY for unauthenticated users)
    if request.method == 'POST':
        from django.contrib.auth import login
        from django.contrib.auth.forms import AuthenticationForm
        
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            
            # Check if student account is approved
            if user.is_student and user.approval_status != 'approved':
                if user.approval_status == 'pending':
                    messages.warning(request, 'Your account is pending approval from an evaluator. Please wait for approval.')
                elif user.approval_status == 'rejected':
                    messages.error(request, 'Your registration has been rejected. Please contact an administrator.')
                form = AuthenticationForm()  # Reset form
            elif not user.is_active:
                messages.error(request, 'Your account is inactive. Please contact an administrator.')
                form = AuthenticationForm()  # Reset form
            else:
                # Login successful - redirect to dashboard immediately
                login(request, user)
                messages.success(request, f'Welcome, {user.get_full_name() or user.username}!')
                
                # Redirect based on role - NEVER back to home
                if user.is_admin:
                    return redirect('reports:admin_dashboard')
                elif user.is_student:
                    return redirect('reports:student_dashboard')
                elif user.is_evaluator:
                    return redirect('reports:evaluator_dashboard')
                # If no role, logout and show login again
                logout(request)
                messages.error(request, 'Invalid user role. Please contact administrator.')
    else:
        from django.contrib.auth.forms import AuthenticationForm
        form = AuthenticationForm()
    
    # Render home page with login form ONLY (no dashboard content)
    response = render(request, 'accounts/home.html', {'form': form})
    
    # Add comprehensive no-cache headers to prevent browser caching
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0, private'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    response['X-Frame-Options'] = 'DENY'
    
    # Only delete session cookie if user is not authenticated (stale cookie)
    if not request.user.is_authenticated:
        response.delete_cookie('sessionid', path='/', domain=None)
    
    # Add timestamp to prevent caching
    response['Last-Modified'] = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())
    
    return response
