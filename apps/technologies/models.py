from django.db import models


class Technology(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50)  # React Icons name like "FaReact"
    color = models.CharField(max_length=20)  # Hex color like "#61DAFB"
    order = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Technology'
        verbose_name_plural = 'Technologies'

    def __str__(self):
        return self.name
