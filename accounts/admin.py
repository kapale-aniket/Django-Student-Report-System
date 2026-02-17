from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for User model"""
    
    list_display = ('username', 'email', 'get_full_name', 'role', 
                   'department', 'batch', 'student_id', 'is_active', 'date_joined')
    list_filter = ('role', 'department', 'batch', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'student_id', 'department')
    ordering = ('-date_joined',)
    actions = ['activate_users', 'deactivate_users', 'generate_random_passwords']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        ('Academic info', {'fields': ('role', 'student_id', 'department', 'batch')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 
                                   'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'role',
                      'student_id', 'department', 'batch', 'phone_number',
                      'password1', 'password2'),
        }),
    )
    
    def activate_users(self, request, queryset):
        """Activate selected users"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} users were successfully activated.')
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        """Deactivate selected users"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} users were successfully deactivated.')
    deactivate_users.short_description = "Deactivate selected users"
    
    def generate_random_passwords(self, request, queryset):
        """Generate random passwords for selected users"""
        import secrets
        import string
        
        updated_count = 0
        for user in queryset:
            # Generate random password
            password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
            user.set_password(password)
            user.save()
            updated_count += 1
            
            # Log the password (in production, you'd send this via email)
            self.message_user(request, f'Password for {user.username}: {password}')
        
        self.message_user(request, f'Generated passwords for {updated_count} users.')
    generate_random_passwords.short_description = "Generate random passwords"