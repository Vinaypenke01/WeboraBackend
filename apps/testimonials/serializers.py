from rest_framework import serializers
from .models import Testimonial


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'name', 'company', 'role', 'content', 'rating', 'avatar', 'featured', 'order', 'active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
