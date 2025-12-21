from rest_framework import viewsets, permissions
from .models import Service
from .serializers import ServiceSerializer
from .services import AppService

class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return AppService.get_all_services()

    def perform_create(self, serializer):
        AppService.create_service(serializer.validated_data)

    def perform_update(self, serializer):
        AppService.update_service(serializer.instance, serializer.validated_data)

    def perform_destroy(self, instance):
        AppService.delete_service(instance)
