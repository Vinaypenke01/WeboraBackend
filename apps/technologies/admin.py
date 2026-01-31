from django.contrib import admin
from .models import Technology


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'color', 'order', 'active']
    list_filter = ['active']
    search_fields = ['name', 'icon']
    list_editable = ['order', 'active']
    ordering = ['order', 'id']
