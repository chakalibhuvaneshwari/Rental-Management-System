from django.contrib import admin
from .models import Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'price', 'property_type', 'is_available', 'owner')
    list_filter = ('city', 'property_type', 'is_available')
    search_fields = ('title', 'location', 'city')
