from django.contrib import admin
from .models import Consent

@admin.register(Consent)
class ConsentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'business_name', 'email', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'email', 'business_name')
    readonly_fields = ('created_at', 'action_date')
