from django.db import models
from django.conf import settings
from vendor.models import VendorProfile

class Booking(models.Model):
    EVENT_TYPE_CHOICES = (
        ('Wedding', 'Wedding'),
        ('Birthday', 'Birthday'),
        ('Corporate', 'Corporate'),
        ('Festival', 'Festival'),
        ('Other', 'Other'),
    )

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_bookings')
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name='vendor_bookings')
    
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)
    event_date = models.DateField()
    event_time = models.TimeField()
    number_of_guests = models.PositiveIntegerField()
    event_location = models.CharField(max_length=255)
    special_requirements = models.TextField(blank=True, null=True)
    
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.vendor and self.number_of_guests:
            self.estimated_price = self.vendor.starting_price_per_plate * self.number_of_guests
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking #{self.id} - {self.customer.full_name} with {self.vendor.business_name}"
