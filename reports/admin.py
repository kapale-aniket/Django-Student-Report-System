from django.contrib import admin
from .models import ProjectReport, Feedback, ReportAssignment


@admin.register(ProjectReport)
class ProjectReportAdmin(admin.ModelAdmin):
    """Admin for ProjectReport model"""
    
    list_display = ('title', 'student', 'department', 'batch', 'status', 
                   'submitted_at', 'file_size')
    list_filter = ('status', 'department', 'batch', 'submitted_at')
    search_fields = ('title', 'student__username', 'student__first_name', 
                    'student__last_name', 'department', 'batch')
    readonly_fields = ('submitted_at', 'updated_at', 'file_size')
    ordering = ('-submitted_at',)
    
    fieldsets = (
        ('Report Information', {
            'fields': ('title', 'description', 'student', 'department', 'batch', 'supervisor')
        }),
        ('File Information', {
            'fields': ('report_file', 'file_size')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('submitted_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def file_size(self, obj):
        return obj.file_size
    file_size.short_description = 'File Size'


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """Admin for Feedback model"""
    
    list_display = ('report', 'evaluator', 'grade', 'max_grade', 'grade_percentage', 'created_at')
    list_filter = ('created_at', 'evaluator', 'report__department', 'report__batch')
    search_fields = ('report__title', 'evaluator__username', 'comments')
    readonly_fields = ('created_at', 'updated_at', 'grade_percentage')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Feedback Information', {
            'fields': ('report', 'evaluator', 'comments')
        }),
        ('Grading', {
            'fields': ('grade', 'max_grade', 'grade_percentage')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def grade_percentage(self, obj):
        return f"{obj.grade_percentage:.1f}%"
    grade_percentage.short_description = 'Grade %'


@admin.register(ReportAssignment)
class ReportAssignmentAdmin(admin.ModelAdmin):
    """Admin for ReportAssignment model"""
    
    list_display = ('report', 'evaluator', 'assigned_by', 'assigned_at', 'is_active')
    list_filter = ('is_active', 'assigned_at', 'evaluator', 'assigned_by')
    search_fields = ('report__title', 'evaluator__username', 'assigned_by__username')
    readonly_fields = ('assigned_at',)
    ordering = ('-assigned_at',)
    
    fieldsets = (
        ('Assignment Information', {
            'fields': ('report', 'evaluator', 'assigned_by', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('assigned_at',),
            'classes': ('collapse',)
        }),
    )