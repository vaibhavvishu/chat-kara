import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatkara_connect.settings')
django.setup()

from vendor.models import VendorProfile
from django.contrib.auth import get_user_model
User = get_user_model()

data = [
    ('Grand Wedding Caterers', 'vijay nagar', 'Specialists in grand wedding catering.', 500.00, '9999900001'),
    ('Palasia Party Foods', 'palasia', 'We cater to birthday and small party events.', 400.00, '9999900002'),
    ('Corporate Eats', 'bhawarkuan', 'Premium corporate event lunches.', 600.00, '9999900003'),
    ('Rau Royal Weddings', 'rau', 'Luxury wedding feasts.', 800.00, '9999900004'),
    ('Super Corridor Bites', 'super corridor', 'Quick party bites and corporate meals.', 350.00, '9999900005'),
    ('Annapurna Sweets & Events', 'annapurna', 'Wedding and birthday specials.', 450.00, '9999900006'),
    ('Nipania Elite', 'nipania', 'High-end corporate and wedding catering.', 950.00, '9999900007'),
    ('Vijay Nagar Birthday Bash', 'vijay nagar', 'Best Birthday and Party catering around.', 600.00, '9999900008'),
]

for name, area, desc, price, phone in data:
    email = f'{name.lower().replace(" ", "_")}@temp.com'
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User.objects.create_user(email=email, full_name=name, phone_number=phone, role='Vendor', password='password123')
    
    VendorProfile.objects.update_or_create(
        user=user,
        defaults={
            'business_name': name,
            'service_area': area,
            'business_description': desc,
            'starting_price_per_plate': price,
            'is_verified': True
        }
    )
    
print('Mock caterers injected successfully!')
