import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatkara_connect.settings')

import django
django.setup()

from booking.models import Booking
from booking.payment_models import Payment
from accounts.models import User
from vendor.models import VendorProfile

print("=== USERS ===")
for u in User.objects.all():
    print(f"  ID:{u.id} | {u.email} | {u.full_name} | {u.role}")

print("\n=== VENDOR PROFILES ===")
for v in VendorProfile.objects.all():
    print(f"  ID:{v.id} | {v.business_name} | verified:{v.is_verified} | price/plate:{v.starting_price_per_plate}")

print("\n=== BOOKINGS ===")
for b in Booking.objects.all():
    print(f"  ID:{b.id} | customer:{b.customer.full_name} | vendor:{b.vendor.business_name} | status:{b.status} | price:{b.estimated_price}")

print("\n=== PAYMENTS ===")
for p in Payment.objects.all():
    print(f"  ID:{p.id} | booking:{p.booking_id} | status:{p.payment_status} | amount:{p.amount}")

# If no bookings exist, create test data
if Booking.objects.count() == 0:
    print("\n--- Creating test booking ---")
    customer = User.objects.filter(role='Customer').first()
    vendor = VendorProfile.objects.filter(is_verified=True).first()
    if customer and vendor:
        from datetime import date, time
        booking = Booking.objects.create(
            customer=customer,
            vendor=vendor,
            event_type='Wedding',
            event_date=date(2026, 12, 25),
            event_time=time(19, 0),
            number_of_guests=100,
            event_location='Test Venue',
            status='Accepted',
        )
        print(f"  Created booking #{booking.id} - status: {booking.status}, price: {booking.estimated_price}")
    else:
        print(f"  Cannot create booking: customer={customer}, vendor={vendor}")

# If bookings exist but none accepted, mark one as Accepted
elif not Booking.objects.filter(status='Accepted').exists():
    booking = Booking.objects.first()
    if booking:
        booking.status = 'Accepted'
        booking.save()
        print(f"\n--- Marked booking #{booking.id} as Accepted ---")
