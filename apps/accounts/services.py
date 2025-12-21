from django.contrib.auth import get_user_model

User = get_user_model()

class UserService:
    @staticmethod
    def get_user_by_id(user_id):
        return User.objects.get(id=user_id)

    @staticmethod
    def create_superuser(username, email, password):
        if User.objects.filter(username=username).exists():
            raise ValueError("Username already exists")
        if User.objects.filter(email=email).exists():
            raise ValueError("Email already exists")
        
        user = User.objects.create_superuser(username=username, email=email, password=password)
        return user
