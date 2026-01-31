from rest_framework import serializers
from .models import Technology


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = ['id', 'name', 'icon', 'color', 'order', 'active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
