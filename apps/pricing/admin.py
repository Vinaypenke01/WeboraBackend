from django.contrib import admin
from .models import PricingPlan


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'popular', 'order', 'active']
    list_filter = ['popular', 'active']
    search_fields = ['name', 'description']
    list_editable = ['order', 'popular', 'active']
    ordering = ['order', 'id']
