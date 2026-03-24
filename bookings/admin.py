from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('property', 'tenant', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('property__title', 'tenant__username')
