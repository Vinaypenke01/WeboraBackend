from rest_framework import viewsets, permissions
from .models import Project
from .serializers import ProjectSerializer
from .services import ProjectService

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return ProjectService.get_all_projects()

    def perform_create(self, serializer):
        ProjectService.create_project(serializer.validated_data)

    def perform_update(self, serializer):
        ProjectService.update_project(serializer.instance, serializer.validated_data)

    def perform_destroy(self, instance):
        ProjectService.delete_project(instance)
