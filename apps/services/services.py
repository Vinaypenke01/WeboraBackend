from django.shortcuts import get_object_or_404
from .models import Service

class AppService: # Renamed to avoid confusion with the app name 'services'
    @staticmethod
    def get_all_services():
        return Service.objects.all()

    @staticmethod
    def get_service_by_id(service_id):
        return get_object_or_404(Service, id=service_id)

    @staticmethod
    def create_service(data):
        return Service.objects.create(**data)

    @staticmethod
    def update_service(service_instance, data):
        for key, value in data.items():
            setattr(service_instance, key, value)
        service_instance.save()
        return service_instance

    @staticmethod
    def delete_service(service_instance):
        service_instance.delete()
