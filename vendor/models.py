from django.db import models
from django.conf import settings

class VendorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vendor_profile')
    business_name = models.CharField(max_length=255)
    business_description = models.TextField(blank=True, null=True)
    service_area = models.CharField(max_length=100)
    address = models.TextField()
    profile_image = models.ImageField(upload_to='vendor/profile/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='vendor/covers/', blank=True, null=True)
    starting_price_per_plate = models.DecimalField(max_digits=10, decimal_places=2)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name


class MenuCategory(models.Model):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Menu Categories'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.vendor.business_name})"


class MenuItem(models.Model):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name='menu_items')
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price_per_plate = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='vendor/menu/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.vendor.business_name}"
