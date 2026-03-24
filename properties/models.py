from django.db import models
from django.conf import settings

class Property(models.fields.related.ForeignKey):
    pass # Wait, let me just write the model directly

class Property(models.Model):
    PROPERTY_TYPES = (
        ('1BHK', '1BHK'),
        ('2BHK', '2BHK'),
        ('3BHK', '3BHK'),
        ('4BHK', '4BHK'),
        ('VILLA', 'Villa'),
    )
    ROOM_TYPES = (
        ('INDIVIDUAL', 'Individual'),
        ('SHARING', 'Sharing'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    city = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    room_type = models.CharField(max_length=50, choices=ROOM_TYPES)
    sharing_capacity = models.IntegerField(default=1)
    amenities = models.TextField(help_text="Comma-separated amenities")
    image = models.ImageField(upload_to='properties/', blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
