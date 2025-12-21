from .models import Message

class MessageService:
    @staticmethod
    def create_message(data):
        return Message.objects.create(**data)

    @staticmethod
    def get_all_messages():
        return Message.objects.all().order_by('-createdAt')

    @staticmethod
    def mark_message_as_read(message_instance):
        message_instance.read = True
        message_instance.save()
        return message_instance
