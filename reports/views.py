from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.http import JsonResponse, Http404, FileResponse, HttpResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache
from django.utils import timezone
from django.conf import settings
import os
import logging

logger = logging.getLogger(__name__)
from .models import ProjectReport, Feedback, ReportAssignment, EvaluatorStudentAssignment
from .forms import (
    ProjectReportForm,
    FeedbackForm,
    ReportAssignmentForm,
    ReportFilterForm,
    CreateEvaluatorForm,
    CreateStudentForm,
    AssignStudentsToEvaluatorForm,
)
from accounts.models import User


@login_required
def dashboard_view(request):
    """Main dashboard view with role-based content"""
    user = request.user
    
    if user.is_student:
        return redirect('reports:student_dashboard')
    elif user.is_evaluator:
        return redirect('reports:evaluator_dashboard')
    elif user.is_admin:
        return redirect('reports:admin_dashboard')
    
    return render(request, 'reports/dashboard.html')


@login_required
@never_cache
def student_dashboard(request):
    """Student dashboard showing their submitted reports"""
    if not request.user.is_student:
        raise Http404("Access denied")
    
    reports = ProjectReport.objects.filter(student=request.user).order_by('-submitted_at')
    
    # Get statistics
    total_reports = reports.count()
    evaluated_reports = reports.filter(status='evaluated').count()
    pending_reports = reports.filter(status__in=['submitted', 'under_review']).count()
    
    context = {
        'reports': reports,
        'total_reports': total_reports,
        'evaluated_reports': evaluated_reports,
        'pending_reports': pending_reports,
    }
    return render(request, 'reports/student_dashboard.html', context)


@login_required
@never_cache
def evaluator_dashboard(request):
    """Evaluator dashboard showing assigned reports and pending students"""
    if not request.user.is_evaluator:
        raise Http404("Access denied")
    
    # Get assigned reports (either via ReportAssignment or EvaluatorStudentAssignment)
    assigned_reports = ProjectReport.objects.filter(
        Q(assignments__evaluator=request.user, assignments__is_active=True)
        | Q(student__in=User.objects.filter(student_evaluator_mappings__evaluator=request.user, student_evaluator_mappings__is_active=True))
    ).distinct().order_by('-submitted_at')
    
    # Get pending students for approval
    pending_students_count = User.objects.filter(role='student', approval_status='pending').count()
    
    # Get statistics
    total_assigned = assigned_reports.count()
    evaluated_count = assigned_reports.filter(feedbacks__evaluator=request.user).count()
    pending_count = total_assigned - evaluated_count
    
    context = {
        'assigned_reports': assigned_reports,
        'total_assigned': total_assigned,
        'evaluated_count': evaluated_count,
        'pending_count': pending_count,
        'pending_students_count': pending_students_count,
    }
    return render(request, 'reports/evaluator_dashboard.html', context)


@login_required
@never_cache
def admin_dashboard(request):
    """Admin dashboard with system overview"""
    if not request.user.is_admin:
        raise Http404("Access denied")
    
    # Get statistics
    total_reports = ProjectReport.objects.count()
    total_students = User.objects.filter(role='student').count()
    total_evaluators = User.objects.filter(role='evaluator').count()
    
    # Filter parameters
    filter_type = request.GET.get('filter', 'all')
    evaluator_filter = request.GET.get('evaluator')
    status_filter = request.GET.get('status')
    department_filter = request.GET.get('department')
    batch_filter = request.GET.get('batch')
    student_filter = request.GET.get('student')
    
    # Get reports based on filter
    reports = ProjectReport.objects.all()
    
    if filter_type == 'recent':
        reports = reports.order_by('-submitted_at')[:20]
    elif filter_type == 'pending':
        reports = reports.filter(status__in=['submitted', 'under_review'])
    elif filter_type == 'approved':
        reports = reports.filter(status='evaluated')
    elif filter_type == 'needs_update':
        reports = reports.filter(status='rejected')
    
    if evaluator_filter:
        reports = reports.filter(assignments__evaluator_id=evaluator_filter)
    if status_filter:
        reports = reports.filter(status=status_filter)
    if department_filter:
        reports = reports.filter(department=department_filter)
    if batch_filter:
        reports = reports.filter(batch__icontains=batch_filter)
    if student_filter:
        reports = reports.filter(
            Q(student__first_name__icontains=student_filter)
            | Q(student__last_name__icontains=student_filter)
            | Q(student__username__icontains=student_filter)
        )
    
    # Recent reports
    recent_reports = ProjectReport.objects.order_by('-submitted_at')[:10]
    
    # Department-wise statistics
    dept_stats = ProjectReport.objects.values('department').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Status-wise statistics
    status_stats = ProjectReport.objects.values('status').annotate(
        count=Count('id')
    )
    
    # Evaluator statistics
    evaluator_stats = User.objects.filter(role='evaluator').annotate(
        assigned_count=Count('assigned_reports', filter=Q(assigned_reports__is_active=True)),
        evaluated_count=Count('given_feedbacks')
    )
    
    context = {
        'total_reports': total_reports,
        'total_students': total_students,
        'total_evaluators': total_evaluators,
        'recent_reports': recent_reports,
        'dept_stats': dept_stats,
        'status_stats': status_stats,
        'evaluator_stats': evaluator_stats,
        'filtered_reports': reports[:20],
        'filter_type': filter_type,
        'evaluator_filter': evaluator_filter,
        'status_filter': status_filter,
        'department_filter': department_filter,
        'batch_filter': batch_filter,
        'student_filter': student_filter,
    }
    return render(request, 'reports/admin_dashboard.html', context)


@login_required
def submit_report(request):
    """Submit a new project report with file validation and exception handling"""
    if not request.user.is_student:
        return HttpResponseForbidden("Access denied")
    
    if request.method == 'POST':
        try:
            form = ProjectReportForm(request.POST, request.FILES, user=request.user)
            if form.is_valid():
                report = form.save(commit=False)
                report.student = request.user
                
                # Store original filename before save
                if 'report_file' in request.FILES:
                    original_filename = request.FILES['report_file'].name
                    report._original_filename = original_filename
                    report.original_filename = original_filename
                
                report.save()
                
                # Auto-assign based on explicit mappings first
                mapped_evaluators = User.objects.filter(
                    evaluator_student_mappings__student=request.user,
                    evaluator_student_mappings__is_active=True
                )
                if mapped_evaluators.exists():
                    for evaluator in mapped_evaluators:
                        ReportAssignment.objects.get_or_create(
                            report=report,
                            evaluator=evaluator,
                            defaults={'assigned_by': request.user, 'is_active': True}
                        )
                else:
                    # Fallback: assign evaluators from same department
                    evaluators = User.objects.filter(role='evaluator', department=report.department)
                    for evaluator in evaluators:
                        ReportAssignment.objects.get_or_create(
                            report=report,
                            evaluator=evaluator,
                            defaults={'assigned_by': request.user, 'is_active': True}
                        )
                messages.success(request, 'Report submitted successfully!')
                return redirect('reports:student_dashboard')
        except Exception as e:
            logger.error(f"Error submitting report: {str(e)}")
            messages.error(request, 'An error occurred while submitting the report. Please try again.')
    else:
        form = ProjectReportForm(user=request.user)
    
    return render(request, 'reports/submit_report.html', {'form': form})


@login_required
def report_detail(request, report_id):
    """View report details"""
    report = get_object_or_404(ProjectReport, id=report_id)
    
    # Check access permissions
    if request.user.is_student and report.student != request.user:
        raise Http404("Access denied")
    # Evaluators are allowed to view report details regardless of assignment.
    # Evaluation actions remain restricted in templates and feedback view.
    
    # Get feedback for this report
    feedbacks = Feedback.objects.filter(report=report).order_by('-created_at')
    
    # Check if current user has given feedback
    user_feedback = None
    if request.user.is_evaluator:
        try:
            user_feedback = Feedback.objects.get(report=report, evaluator=request.user)
        except Feedback.DoesNotExist:
            pass
    
    # Build helper list: evaluator IDs who have given feedback
    evaluated_evaluator_ids = list(
        Feedback.objects.filter(report=report).values_list('evaluator_id', flat=True)
    )

    context = {
        'report': report,
        'feedbacks': feedbacks,
        'user_feedback': user_feedback,
        'evaluated_evaluator_ids': evaluated_evaluator_ids,
    }
    return render(request, 'reports/report_detail.html', context)

@login_required
def give_feedback(request, report_id):
    if not request.user.is_evaluator:
        raise Http404("Access denied")

    report = get_object_or_404(ProjectReport, id=report_id)

    feedback, created = Feedback.objects.get_or_create(
        report=report,
        evaluator=request.user,
        defaults={'comments': '', 'grade': None, 'max_grade': 100.00}
    )

    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            report.status = 'evaluated' if feedback.grade is not None else 'under_review'
            report.save()
            messages.success(request, 'Feedback submitted successfully!')
            return redirect('reports:report_detail', report_id=report.id)
    else:
        form = FeedbackForm(instance=feedback)

    return render(request, 'reports/give_feedback.html', {
        'form': form,
        'report': report,
        'feedback': feedback,
    })


@login_required
def all_reports(request):
    """View all reports with filtering (admin and evaluator access)"""
    if not (request.user.is_admin or request.user.is_evaluator):
        raise Http404("Access denied")
    
    reports = ProjectReport.objects.all().order_by('-submitted_at')
    
    # Apply filters
    filter_form = ReportFilterForm(request.GET)
    if filter_form.is_valid():
        department = filter_form.cleaned_data.get('department')
        batch = filter_form.cleaned_data.get('batch')
        status = filter_form.cleaned_data.get('status')
        student = filter_form.cleaned_data.get('student')
        
        if department:
            reports = reports.filter(department=department)
        if batch:
            reports = reports.filter(batch__icontains=batch)
        if status:
            reports = reports.filter(status=status)
        if student:
            reports = reports.filter(
                Q(student__first_name__icontains=student) |
                Q(student__last_name__icontains=student) |
                Q(student__username__icontains=student)
            )
    
    # Pagination
    paginator = Paginator(reports, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'filter_form': filter_form,
    }
    return render(request, 'reports/all_reports.html', context)


@login_required
def assign_evaluator(request, report_id):
    """Assign evaluator to a report (admin only)"""
    if not request.user.is_admin:
        raise Http404("Access denied")
    
    report = get_object_or_404(ProjectReport, id=report_id)
    
    if request.method == 'POST':
        form = ReportAssignmentForm(request.POST, report=report)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.report = report
            assignment.assigned_by = request.user
            assignment.save()
            messages.success(request, f'Report assigned to {assignment.evaluator.username}')
            return redirect('reports:report_detail', report_id=report.id)
    else:
        form = ReportAssignmentForm(report=report)
    
    context = {
        'form': form,
        'report': report,
    }
    return render(request, 'reports/assign_evaluator.html', context)


@login_required
def user_management(request):
    """User management page (admin only)"""
    if not request.user.is_admin:
        raise Http404("Access denied")
    
    users = User.objects.all().order_by('-date_joined')
    
    # Filter by role
    role_filter = request.GET.get('role')
    if role_filter:
        users = users.filter(role=role_filter)
    
    # Pagination
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'role_filter': role_filter,
    }
    return render(request, 'reports/user_management.html', context)


@login_required
def admin_add_evaluator(request):
    """Admin creates evaluator accounts with automatic email password delivery"""
    if not request.user.is_admin:
        return HttpResponseForbidden("Access denied")
    if request.method == 'POST':
        try:
            form = CreateEvaluatorForm(request.POST)
            if form.is_valid():
                evaluator = form.save()
                password = getattr(evaluator, '_temp_password', None)
                email_sent = getattr(evaluator, '_email_sent', False)
                email_error = getattr(evaluator, '_email_error', None)
                
                if email_sent and evaluator.email:
                    messages.success(request, f"Evaluator '{evaluator.username}' created successfully. Login credentials have been sent to {evaluator.email}.")
                elif password:
                    messages.warning(request, 
                        f"Evaluator '{evaluator.username}' created, but email could not be sent. "
                        f"Please provide the credentials manually:\n"
                        f"Username: {evaluator.username}\n"
                        f"Password: {password}")
                    if email_error:
                        error_msg = f"Email error: {email_error}"
                        # Add helpful message for Gmail authentication errors
                        if '535' in str(email_error) or 'BadCredentials' in str(email_error) or 'Username and Password not accepted' in str(email_error):
                            error_msg += "\n\n⚠️ Gmail requires an App Password (not regular password). See FIX_EMAIL_IMMEDIATELY.md for instructions."
                        messages.error(request, error_msg)
                else:
                    messages.warning(request, f"Evaluator '{evaluator.username}' created, but no email was provided and password generation failed.")
                
                return redirect('reports:user_management')
            else:
                # Form is invalid - errors will be displayed in template
                messages.error(request, "Please correct the errors below.")
        except Exception as e:
            logger.error(f"Error creating evaluator: {str(e)}", exc_info=True)
            messages.error(request, f"An error occurred while creating the evaluator: {str(e)}")
    else:
        form = CreateEvaluatorForm()
    return render(request, 'reports/admin_add_evaluator.html', {'form': form})


@login_required
def evaluator_add_student(request):
    """Evaluator creates student accounts with automatic email password delivery"""
    if not request.user.is_evaluator:
        return HttpResponseForbidden("Access denied")
    if request.method == 'POST':
        try:
            form = CreateStudentForm(request.POST)
            if form.is_valid():
                student = form.save()
                password = getattr(student, '_temp_password', None)
                email_sent = getattr(student, '_email_sent', False)
                email_error = getattr(student, '_email_error', None)
                
                EvaluatorStudentAssignment.objects.get_or_create(
                    evaluator=request.user,
                    student=student,
                    defaults={'assigned_by': request.user, 'is_active': True}
                )
                
                if email_sent and student.email:
                    messages.success(request, f"Student '{student.username}' created and linked to you. Login credentials have been sent to {student.email}.")
                elif password:
                    messages.warning(request, 
                        f"Student '{student.username}' created and linked to you, but email could not be sent. "
                        f"Please provide the credentials manually:\n"
                        f"Username: {student.username}\n"
                        f"Password: {password}")
                    if email_error:
                        error_msg = f"Email error: {email_error}"
                        # Add helpful message for Gmail authentication errors
                        if '535' in str(email_error) or 'BadCredentials' in str(email_error) or 'Username and Password not accepted' in str(email_error):
                            error_msg += "\n\n⚠️ Gmail requires an App Password (not regular password). See FIX_EMAIL_IMMEDIATELY.md for instructions."
                        messages.error(request, error_msg)
                else:
                    messages.warning(request, f"Student '{student.username}' created, but password generation failed.")
                return redirect('reports:evaluator_dashboard')
        except Exception as e:
            logger.error(f"Error creating student: {str(e)}")
            messages.error(request, f"An error occurred while creating the student: {str(e)}")
    else:
        form = CreateStudentForm()
    return render(request, 'reports/evaluator_add_student.html', {'form': form})


@login_required
def pending_students(request):
    """View pending student registrations that need approval"""
    if not request.user.is_evaluator:
        return HttpResponseForbidden("Access denied")
    
    # Get students pending approval
    pending_students_list = User.objects.filter(
        role='student',
        approval_status='pending'
    ).order_by('-created_at')
    
    context = {
        'pending_students': pending_students_list,
    }
    return render(request, 'reports/pending_students.html', context)


@login_required
def approve_student(request, student_id):
    """Approve a pending student registration"""
    if not request.user.is_evaluator:
        return HttpResponseForbidden("Access denied")
    
    student = get_object_or_404(User, id=student_id, role='student', approval_status='pending')
    
    if request.method == 'POST':
        student.approval_status = 'approved'
        student.is_active = True
        student.approved_by = request.user
        student.approval_date = timezone.now()
        student.save()
        
        # Create evaluator-student assignment
        EvaluatorStudentAssignment.objects.get_or_create(
            evaluator=request.user,
            student=student,
            defaults={'assigned_by': request.user, 'is_active': True}
        )
        
        # Send approval notification email to student
        if student.email:
            try:
                from django.core.mail import send_mail
                from django.template.loader import render_to_string
                from django.urls import reverse
                login_url = f"{getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')}{reverse('accounts:login')}"
                
                html_message = render_to_string('emails/student_approved.html', {
                    'first_name': student.first_name or student.username,
                    'username': student.username,
                    'login_url': login_url,
                    'year': timezone.now().year,
                })
                send_mail(
                    subject='Your Student Account Has Been Approved - Student Report System',
                    message=f"Hello {student.first_name or student.username},\n\nYour student account has been approved!\nUsername: {student.username}\n\nYou can now log in at {login_url} and start submitting your reports.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[student.email],
                    html_message=html_message,
                    fail_silently=False,
                )
            except Exception as e:
                logger.error(f"Failed to send approval email to {student.email}: {str(e)}")
        
        messages.success(request, f"Student '{student.username}' has been approved and can now access the system.")
        return redirect('reports:pending_students')
    
    context = {
        'student': student,
    }
    return render(request, 'reports/approve_student.html', context)


@login_required
def reject_student(request, student_id):
    """Reject a pending student registration"""
    if not request.user.is_evaluator:
        return HttpResponseForbidden("Access denied")
    
    student = get_object_or_404(User, id=student_id, role='student', approval_status='pending')
    
    if request.method == 'POST':
        student.approval_status = 'rejected'
        student.is_active = False
        student.save()
        
        messages.info(request, f"Student registration for '{student.username}' has been rejected.")
        return redirect('reports:pending_students')
    
    context = {
        'student': student,
    }
    return render(request, 'reports/reject_student.html', context)


@login_required
def admin_assign_students(request):
    if not request.user.is_admin:
        raise Http404("Access denied")
    if request.method == 'POST':
        form = AssignStudentsToEvaluatorForm(request.POST)
        if form.is_valid():
            evaluator = form.cleaned_data['evaluator']
            students = form.cleaned_data['students']
            created = 0
            for student in students:
                _, was_created = EvaluatorStudentAssignment.objects.get_or_create(
                    evaluator=evaluator,
                    student=student,
                    defaults={'assigned_by': request.user, 'is_active': True}
                )
                if was_created:
                    created += 1
            messages.success(request, f"Assigned {created} students to {evaluator.username}")
            return redirect('reports:user_management')
    else:
        form = AssignStudentsToEvaluatorForm()
    return render(request, 'reports/admin_assign_students.html', {'form': form})


@login_required
def admin_delete_evaluator(request, evaluator_id):
    """Admin deletes an evaluator - completely removes from database"""
    if not request.user.is_admin:
        return HttpResponseForbidden("Access denied")
    
    try:
        evaluator = get_object_or_404(User, id=evaluator_id, role='evaluator')
        
        if request.method == 'POST':
            evaluator_username = evaluator.username
            evaluator_email = evaluator.email
            
            # Delete the evaluator - Django CASCADE will handle all related records
            # This will automatically delete:
            # - EvaluatorStudentAssignment records
            # - ReportAssignment records  
            # - Feedback records (if any)
            # - All related data
            evaluator.delete()
            
            messages.success(request, f"Evaluator '{evaluator_username}' has been completely deleted from the database. You can now create a new evaluator with the same username/email if needed.")
            logger.info(f"Admin {request.user.username} deleted evaluator {evaluator_username} (ID: {evaluator_id})")
            return redirect('reports:user_management')
        
        # Get related data counts for display
        from .models import EvaluatorStudentAssignment, ReportAssignment, Feedback
        assigned_students_count = EvaluatorStudentAssignment.objects.filter(evaluator=evaluator, is_active=True).count()
        assigned_reports_count = ReportAssignment.objects.filter(evaluator=evaluator, is_active=True).count()
        feedback_count = Feedback.objects.filter(evaluator=evaluator).count()
        
        context = {
            'evaluator': evaluator,
            'assigned_students_count': assigned_students_count,
            'assigned_reports_count': assigned_reports_count,
            'feedback_count': feedback_count,
        }
        return render(request, 'reports/admin_delete_evaluator.html', context)
    except Exception as e:
        logger.error(f"Error deleting evaluator {evaluator_id}: {str(e)}", exc_info=True)
        messages.error(request, f"An error occurred while deleting the evaluator: {str(e)}")
        return redirect('reports:user_management')


@login_required
def evaluator_view_students(request):
    """Evaluator views list of their assigned students"""
    if not request.user.is_evaluator:
        return HttpResponseForbidden("Access denied")
    
    # Get students assigned to this evaluator
    assigned_students = User.objects.filter(
        student_evaluator_mappings__evaluator=request.user,
        student_evaluator_mappings__is_active=True
    ).distinct().order_by('-date_joined')
    
    # Get student statistics
    students_with_reports = []
    for student in assigned_students:
        reports_count = ProjectReport.objects.filter(student=student).count()
        students_with_reports.append({
            'student': student,
            'reports_count': reports_count,
        })
    
    context = {
        'students_with_reports': students_with_reports,
    }
    return render(request, 'reports/evaluator_view_students.html', context)


@login_required
def evaluator_delete_student(request, student_id):
    """Evaluator deletes a student - completely removes from database"""
    if not request.user.is_evaluator:
        return HttpResponseForbidden("Access denied")
    
    try:
        student = get_object_or_404(User, id=student_id, role='student')
        
        # Check if student is assigned to this evaluator
        assignment = EvaluatorStudentAssignment.objects.filter(
            evaluator=request.user,
            student=student,
            is_active=True
        ).first()
        
        if not assignment:
            messages.error(request, "You don't have permission to delete this student.")
            return redirect('reports:evaluator_view_students')
        
        if request.method == 'POST':
            student_username = student.username
            student_email = student.email
            
            # Delete the student - Django CASCADE will handle all related records
            # This will automatically delete:
            # - ProjectReport records (and their files)
            # - EvaluatorStudentAssignment records
            # - Feedback records
            # - All related data
            student.delete()
            
            messages.success(request, f"Student '{student_username}' has been completely deleted from the database. You can now create a new student with the same username/email if needed.")
            logger.info(f"Evaluator {request.user.username} deleted student {student_username} (ID: {student_id})")
            return redirect('reports:evaluator_view_students')
        
        # Get related data counts for display
        from .models import ProjectReport
        reports_count = ProjectReport.objects.filter(student=student).count()
        
        context = {
            'student': student,
            'reports_count': reports_count,
        }
        return render(request, 'reports/evaluator_delete_student.html', context)
    except Exception as e:
        logger.error(f"Error deleting student {student_id}: {str(e)}", exc_info=True)
        messages.error(request, f"An error occurred while deleting the student: {str(e)}")
        return redirect('reports:evaluator_view_students')


@login_required
def download_report(request, report_id):
    """Download a report file with access control"""
    try:
        report = get_object_or_404(ProjectReport, id=report_id)
        
        # Check access permissions - Admin can access all files
        if request.user.is_admin:
            pass  # Admin has full access
        elif request.user.is_student and report.student != request.user:
            return HttpResponseForbidden("You don't have access to this file")
        elif request.user.is_evaluator:
            if not report.assignments.filter(evaluator=request.user, is_active=True).exists():
                return HttpResponseForbidden("You don't have access to this file")
        
        # Get the file path
        file_path = os.path.join(settings.MEDIA_ROOT, report.report_file.name)
        
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path} for report {report_id}")
            raise Http404("File not found")
        
        # Get original filename or use UUID filename
        original_filename = getattr(report, '_original_filename', None) or report.filename
        
        # Create file response
        response = FileResponse(
            open(file_path, 'rb'),
            as_attachment=True,
            filename=original_filename
        )
        
        return response
    except Exception as e:
        logger.error(f"Error downloading report {report_id}: {str(e)}")
        raise Http404("Error accessing file")


@login_required
def view_report(request, report_id):
    """View a report file in browser with access control"""
    try:
        report = get_object_or_404(ProjectReport, id=report_id)
        
        # Check access permissions - Admin can access all files
        if request.user.is_admin:
            pass  # Admin has full access
        elif request.user.is_student and report.student != request.user:
            return HttpResponseForbidden("You don't have access to this file")
        # Evaluators are allowed to view the file regardless of assignment.
        
        # Get the file path
        file_path = os.path.join(settings.MEDIA_ROOT, report.report_file.name)
        
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path} for report {report_id}")
            raise Http404("File not found")
        
        # Determine content type based on file extension
        file_extension = os.path.splitext(report.filename)[1].lower()
        
        if file_extension == '.pdf':
            content_type = 'application/pdf'
        elif file_extension == '.docx':
            content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        elif file_extension == '.doc':
            content_type = 'application/msword'
        elif file_extension == '.xlsx':
            content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        elif file_extension == '.txt':
            content_type = 'text/plain'
        else:
            content_type = 'application/octet-stream'
        
        # Create file response for viewing
        response = FileResponse(
            open(file_path, 'rb'),
            content_type=content_type
        )
        
        return response
    except Exception as e:
        logger.error(f"Error viewing report {report_id}: {str(e)}")
        raise Http404("Error accessing file")