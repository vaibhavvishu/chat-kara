from django.contrib import admin
from .models import VendorProfile, MenuCategory, MenuItem

@admin.register(VendorProfile)
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'service_area', 'is_verified', 'created_at')
    list_filter = ('is_verified', 'service_area')
    search_fields = ('business_name', 'user__username', 'service_area')

@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'created_at')
    search_fields = ('name', 'vendor__business_name')
    list_filter = ('created_at',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'category', 'price_per_plate', 'is_available')
    list_filter = ('is_available', 'category')
    search_fields = ('name', 'vendor__business_name', 'category__name')
