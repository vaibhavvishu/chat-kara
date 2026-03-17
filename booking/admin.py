from django.contrib import admin
from .models import Booking
from .payment_models import Payment


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'vendor', 'event_type', 'event_date', 'status', 'created_at')
    list_filter = ('status', 'event_type', 'event_date')
    search_fields = ('customer__full_name', 'vendor__business_name', 'event_location')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'customer', 'amount', 'payment_method', 'payment_status', 'stripe_payment_id', 'created_at')
    list_filter = ('payment_status', 'payment_method', 'created_at')
    search_fields = ('customer__full_name', 'booking__vendor__business_name', 'stripe_payment_id')
    readonly_fields = ('stripe_payment_id', 'created_at', 'updated_at')
    raw_id_fields = ('booking', 'customer')
