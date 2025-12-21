from django.db import models

class Message(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)  # CamelCase match
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"
