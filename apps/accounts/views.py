from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from .services import UserService

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Add custom claims
        data['user'] = UserSerializer(self.user).data
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserMeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
        # Note: request.user is already authenticated and retrieved by middleware/DRF.
        # Calling UserService.get_user_by_id(self.request.user.id) would be redundant DB hit.
        # But we adhere to the pattern where logic resides in service if complex.
        # For 'me' endpoint, returning request.user is standard. 
        # If we strictly must use service:
        # return UserService.get_user_by_id(self.request.user.id) 

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        return Response({"success": True}, status=status.HTTP_200_OK)
