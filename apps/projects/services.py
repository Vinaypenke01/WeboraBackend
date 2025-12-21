from django.shortcuts import get_object_or_404
from .models import Project

class ProjectService:
    @staticmethod
    def get_all_projects():
        return Project.objects.all()

    @staticmethod
    def get_project_by_id(project_id):
        return get_object_or_404(Project, id=project_id)

    @staticmethod
    def create_project(data):
        return Project.objects.create(**data)

    @staticmethod
    def update_project(project_instance, data):
        for key, value in data.items():
            setattr(project_instance, key, value)
        project_instance.save()
        return project_instance

    @staticmethod
    def delete_project(project_instance):
        project_instance.delete()
