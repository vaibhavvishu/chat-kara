from django.urls import path
from . import views
from . import payment_views

urlpatterns = [
    path('book/<int:vendor_id>/', views.create_booking, name='create_booking'),
    path('customer/bookings/', views.customer_booking_history, name='customer_booking_history'),
    path('customer/booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('vendor/bookings/', views.vendor_booking_requests, name='vendor_booking_requests'),
    path('vendor/booking/<int:booking_id>/update-status/', views.update_booking_status, name='update_booking_status'),

    # Payment URLs
    path('payment/<int:booking_id>/', payment_views.payment_page, name='payment_page'),
    path('payment/<int:booking_id>/checkout/', payment_views.create_checkout_session, name='create_checkout_session'),
    path('payment/success/', payment_views.payment_success, name='payment_success'),
    path('payment/cancel/', payment_views.payment_cancel, name='payment_cancel'),
    path('customer/payments/', payment_views.customer_payments, name='customer_payments'),
    path('payment/webhook/', payment_views.stripe_webhook, name='stripe_webhook'),
]
