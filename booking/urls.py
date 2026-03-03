from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:vendor_id>/', views.create_booking, name='create_booking'),
    path('customer/bookings/', views.customer_booking_history, name='customer_booking_history'),
    path('customer/booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('vendor/bookings/', views.vendor_booking_requests, name='vendor_booking_requests'),
    path('vendor/booking/<int:booking_id>/update-status/', views.update_booking_status, name='update_booking_status'),
]
