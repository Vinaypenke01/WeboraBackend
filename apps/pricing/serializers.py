from rest_framework import serializers
from .models import PricingPlan


class PricingPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingPlan
        fields = ['id', 'name', 'price', 'description', 'features', 'popular', 'order', 'active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
