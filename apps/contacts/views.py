from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer
from .services import MessageService

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return MessageService.get_all_messages()

    def perform_create(self, serializer):
        MessageService.create_message(serializer.validated_data)

    @action(detail=True, methods=['put'], permission_classes=[permissions.IsAdminUser])
    def read(self, request, pk=None):
        message = self.get_object()
        updated_message = MessageService.mark_message_as_read(message)
        return Response(self.get_serializer(updated_message).data)
