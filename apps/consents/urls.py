from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConsentViewSet

router = DefaultRouter()
router.register(r'', ConsentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
