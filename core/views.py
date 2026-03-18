from django.shortcuts import render
from django.db.models import Q
from vendor.models import VendorProfile

def home(request):
    vendors = VendorProfile.objects.filter(is_verified=True).order_by('-created_at')

    # Filtering logic for homepage search
    area = request.GET.get('area')
    if area:
        vendors = vendors.filter(service_area__icontains=area)

    event_type = request.GET.get('event_type')
    if event_type:
        vendors = vendors.filter(
            Q(business_description__icontains=event_type) |
            Q(categories__name__icontains=event_type)
        ).distinct()

    budget = request.GET.get('budget')
    if budget:
        vendors = vendors.filter(starting_price_per_plate__lte=budget)

    # Determine if a search was performed (any filter applied)
    is_search = bool(area or event_type or budget)

    context = {
        'caterers': vendors,
        'request_GET': request.GET,
        'is_search': is_search,
    }
    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')
