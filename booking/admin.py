from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'vendor', 'event_type', 'event_date', 'status', 'created_at')
    list_filter = ('status', 'event_type', 'event_date')
    search_fields = ('customer__full_name', 'vendor__business_name', 'event_location')
