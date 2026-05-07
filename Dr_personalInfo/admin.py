from django.contrib import admin
from .models import DoctorPersonalInfo

@admin.register(DoctorPersonalInfo)
class DoctorPersonalInfoAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'email', 'mobile_number', 'status', 'created_at')
    list_filter = ('status', 'gender', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'mobile_number')
    readonly_fields = ('created_at',)
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'Name'
    
    # Custom actions for quick approval/rejection
    actions = ['approve_doctors', 'reject_doctors']

    @admin.action(description='Approve selected doctors')
    def approve_doctors(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, "Selected doctors have been approved.")

    @admin.action(description='Reject selected doctors')
    def reject_doctors(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, "Selected doctors have been rejected.")
