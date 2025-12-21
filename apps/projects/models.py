from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    description = models.TextField()
    challenge = models.TextField()
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    techStack = models.JSONField(default=list)
    liveLink = models.URLField()
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title
