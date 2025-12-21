from rest_framework import views, permissions, response
from .models import SiteSetting
from .serializers import SiteSettingSerializer
from .services import SiteSettingService

class SiteSettingView(views.APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get(self, request):
        settings = SiteSettingService.get_or_create_settings()
        serializer = SiteSettingSerializer(settings)
        return response.Response(serializer.data)

    def put(self, request):
        settings = SiteSettingService.get_or_create_settings()
        serializer = SiteSettingSerializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            SiteSettingService.update_settings(settings, serializer.validated_data)
            # Re-fetch or reuse updated instance. Serializer already has validated data but let's be safe.
            # Using serializer.save() would work but we want to use the service.
            # However, serializer.save() calls update() on the model instance. 
            # To strictly use service, we pass validated_data to service.
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=400)
