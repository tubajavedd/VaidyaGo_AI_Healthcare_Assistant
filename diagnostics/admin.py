from django.contrib import admin
from .models import Diagnostic

@admin.register(Diagnostic)
class DiagnosticAdmin(admin.ModelAdmin):
    list_display = ('user', 'body_part', 'sub_region', 'confidence_score', 'created_at')
    list_filter = ('body_part', 'severity', 'created_at')
    search_fields = ('user__username', 'body_part', 'sub_region')
    readonly_fields = ('created_at', 'updated_at')
