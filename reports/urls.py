from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('evaluator/', views.evaluator_dashboard, name='evaluator_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    
    # Report management
    path('submit/', views.submit_report, name='submit_report'),
    path('report/<int:report_id>/', views.report_detail, name='report_detail'),
    path('report/<int:report_id>/feedback/', views.give_feedback, name='give_feedback'),
    path('report/<int:report_id>/assign/', views.assign_evaluator, name='assign_evaluator'),
    path('report/<int:report_id>/download/', views.download_report, name='download_report'),
    path('report/<int:report_id>/view/', views.view_report, name='view_report'),
    
    # Admin functions
    path('all-reports/', views.all_reports, name='all_reports'),
    path('users/', views.user_management, name='user_management'),
    path('users/add-evaluator/', views.admin_add_evaluator, name='admin_add_evaluator'),
    path('users/assign-students/', views.admin_assign_students, name='admin_assign_students'),

    # Evaluator functions
    path('students/add/', views.evaluator_add_student, name='evaluator_add_student'),
]

