from django.urls import path
from .views import CustomTokenObtainPairView, UserMeView, LogoutView, CreateAdminStep1View, CreateAdminStep2View

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('me/', UserMeView.as_view(), name='user_me'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create-admin-step1/', CreateAdminStep1View.as_view(), name='create_admin_step1'),
    path('create-admin-step2/', CreateAdminStep2View.as_view(), name='create_admin_step2'),
]
