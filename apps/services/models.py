from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=255)
    icon = models.CharField(max_length=100)
    shortDescription = models.TextField()  # CamelCase to match frontend
    description = models.TextField()
    benefits = models.JSONField(default=list)
    process = models.JSONField(default=list)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
