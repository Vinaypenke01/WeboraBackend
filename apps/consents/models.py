from django.db import models
from django.conf import settings

class Consent(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    )

    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=20)
    business_name = models.CharField(max_length=255)
    is_consented = models.BooleanField(default=False)
    version_number = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Admin actions
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    accepted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='accepted_consents'
    )
    action_date = models.DateTimeField(null=True, blank=True)
    deployment_date = models.DateTimeField(null=True, blank=True, help_text="Actual project deployment date")
    admin_notes = models.TextField(blank=True, null=True)
    
    # Email tracking
    is_final_email_sent = models.BooleanField(default=False)
    final_email_sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Consent from {self.full_name} ({self.business_name})"
