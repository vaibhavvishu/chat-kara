import os, django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatkara_connect.settings')
django.setup()

from vendor.models import VendorProfile
from django.contrib.auth import get_user_model
User = get_user_model()

areas = [
    ('vijay nagar', 'Vijay Nagar'),
    ('palasia', 'Palasia'),
    ('bhawarkuan', 'Bhawarkuan'),
    ('rau', 'Rau'),
    ('super corridor', 'Super Corridor'),
    ('scheme 54', 'Scheme 54'),
    ('bengali square', 'Bengali Square'),
    ('annapurna', 'Annapurna'),
    ('nipania', 'Nipania'),
]

event_types = [
    ('wedding', 'Wedding', 'Premium luxury wedding celebrations and feasts.'),
    ('corporate', 'Corporate', 'Professional corporate events and lunches.'),
    ('birthday', 'Birthday', 'Special birthday party food and snacks.'),
    ('party', 'Small Party', 'Intimate small party and gathering menus.')
]

def generate_db():
    print("Generating comprehensive combinations...")
    count = 0
    for area_val, area_name in areas:
        for ev_val, ev_name, ev_desc in event_types:
            count += 1
            b_name = f"{area_name} {ev_name} Specialists"
            price = round(random.uniform(300, 1500), -1) # Rounds to nearest 10
            
            # Create a unique email and username
            email = f"caterer_{count}_{area_val.replace(' ', '')}{ev_val}@test.com"
            username = f"usr_{count}_{area_val.replace(' ', '')}{ev_val}"
            phone = f"991100{count:04d}"
            
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    email=email,
                    full_name=b_name,
                    phone_number=phone,
                    role='Vendor',
                    password='password123'
                )
            
            VendorProfile.objects.update_or_create(
                user=user,
                defaults={
                    'business_name': b_name,
                    'service_area': area_val, # Use the lowercase value so exact searches will catch it just in case, though icontains handles anything
                    'business_description': f"We are the best in {area_name} for {ev_desc}",
                    'starting_price_per_plate': price,
                    'is_verified': True
                }
            )
            print(f"Created: {b_name} | Area: {area_name} | Price: {price} | Desc: {ev_val}")

    print(f"Successfully generated {count} caterers testing every combination!")

generate_db()
