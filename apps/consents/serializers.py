from rest_framework import serializers
from .models import Consent
from apps.accounts.serializers import UserSerializer

class ConsentSerializer(serializers.ModelSerializer):
    accepted_by_details = UserSerializer(source='accepted_by', read_only=True)

    class Error(serializers.Serializer):
        pass

    class Meta:
        model = Consent
        fields = [
            'id', 'full_name', 'email', 'mobile_number', 'business_name', 
            'is_consented', 'version_number', 'created_at', 'status', 
            'accepted_by', 'accepted_by_details', 'action_date', 'deployment_date', 'maintenance_duration_months', 'admin_notes',
            'is_final_email_sent', 'final_email_sent_at'
        ]
        read_only_fields = ['id', 'created_at', 'accepted_by', 'action_date', 'status']

class ConsentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consent
        fields = ['full_name', 'email', 'mobile_number', 'business_name', 'is_consented']

    def validate_is_consented(self, value):
        if not value:
            raise serializers.ValidationError("Consent must be accepted.")
        return value
