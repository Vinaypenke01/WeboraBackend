from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    excerpt = models.TextField()
    content = models.TextField()
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    tags = models.JSONField(default=list)
    featuredImage = models.ImageField(upload_to='blogs/', blank=True, null=True) # Matching frontend camelCase
    publishedDate = models.DateField(auto_now_add=True) # Matching frontend camelCase
    readTime = models.CharField(max_length=50) # Matching frontend camelCase

    def __str__(self):
        return self.title
