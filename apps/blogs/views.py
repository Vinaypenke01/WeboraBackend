from rest_framework import viewsets, permissions
from .models import Blog
from .serializers import BlogSerializer
from .services import BlogService

class BlogViewSet(viewsets.ModelViewSet):
    serializer_class = BlogSerializer
    lookup_field = 'slug'
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return BlogService.get_all_blogs()

    def get_object(self):
        slug = self.kwargs.get('slug')
        return BlogService.get_blog_by_slug(slug)

    def perform_create(self, serializer):
        BlogService.create_blog(serializer.validated_data)

    def perform_update(self, serializer):
        BlogService.update_blog(serializer.instance, serializer.validated_data)

    def perform_destroy(self, instance):
        BlogService.delete_blog(instance)
