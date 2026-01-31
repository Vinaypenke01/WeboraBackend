from django.contrib import admin
from .models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'role', 'rating', 'featured', 'order', 'active']
    list_filter = ['rating', 'featured', 'active']
    search_fields = ['name', 'company', 'content']
    list_editable = ['order', 'featured', 'active']
    ordering = ['order', '-created_at']
