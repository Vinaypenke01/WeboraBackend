from django.db import models

class SiteSetting(models.Model):
    companyName = models.CharField(max_length=255, default="DigitalCore Solutions")
    tagline = models.CharField(max_length=255, default="Building Your Digital Presence")
    email = models.EmailField(default="info@digitalcoresolutions.com")
    phone = models.CharField(max_length=50, default="+1 (555) 123-4567")
    address = models.TextField(default="123 Tech Street, San Francisco, CA 94102")
    social = models.JSONField(default=dict)
    hero = models.JSONField(default=dict)
    about = models.JSONField(default=dict)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

    def save(self, *args, **kwargs):
        if not self.pk and SiteSetting.objects.exists():
            return SiteSetting.objects.first()
        return super().save(*args, **kwargs)
