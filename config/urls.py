from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('apps.accounts.urls')),
    path('api/v1/projects/', include('apps.projects.urls')),
    path('api/v1/services/', include('apps.services.urls')),
    path('api/v1/blogs/', include('apps.blogs.urls')),
    path('api/v1/messages/', include('apps.contacts.urls')),
    path('api/v1/settings/', include('apps.site_settings.urls')),
    path('api/v1/pricing/', include('apps.pricing.urls')),
    path('api/v1/technologies/', include('apps.technologies.urls')),
    path('api/v1/testimonials/', include('apps.testimonials.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
