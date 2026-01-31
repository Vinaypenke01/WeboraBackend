from django.db import models


class PricingPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=50)
    description = models.TextField()
    features = models.JSONField(default=list)
    popular = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Pricing Plan'
        verbose_name_plural = 'Pricing Plans'

    def __str__(self):
        return self.name
