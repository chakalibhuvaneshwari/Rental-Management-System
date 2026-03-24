from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('TENANT', 'Tenant'),
        ('OWNER', 'Owner'),
        ('ADMIN', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='TENANT')
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.property.title}"

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    property = models.ForeignKey('properties.Property', on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"
