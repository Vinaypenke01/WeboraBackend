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

class CreateAdminStep1View(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if not all([username, email, password, confirm_password]):
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        # Basic Check if user exists
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Simulate generating OTP
        otp = "123456" 
        
        return Response({
            "success": True, 
            "message": "OTP sent to email (simulated)", 
            "otp": otp # Returning OTP for simulation as requested
        }, status=status.HTTP_200_OK)

class CreateAdminStep2View(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        otp = request.data.get('otp')
        
        # In a real app, verify OTP against stored value (Redis/DB)
        if otp != "123456":
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            UserService.create_superuser(username, email, password)
            return Response({"success": True, "message": "Admin user created successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
