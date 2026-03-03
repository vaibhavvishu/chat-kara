from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.utils.text import slugify
from vendor.models import VendorProfile, MenuCategory, MenuItem

def caterer_list(request):
    # Base query for verified vendors
    vendors = VendorProfile.objects.filter(is_verified=True)

    # Filtering logic
    search_query = request.GET.get('search')
    if search_query:
        vendors = vendors.filter(business_name__icontains=search_query)

    city = request.GET.get('city')
    if city:
        vendors = vendors.filter(service_area__icontains=city)

    budget = request.GET.get('budget')
    if budget:
        vendors = vendors.filter(starting_price_per_plate__lte=budget)
        
    category_id = request.GET.get('category')
    if category_id:
        vendors = vendors.filter(categories__id=category_id).distinct()

    # Sorting
    sort_by = request.GET.get('sort')
    if sort_by == 'price_asc':
        vendors = vendors.order_by('starting_price_per_plate')
    elif sort_by == 'price_desc':
        vendors = vendors.order_by('-starting_price_per_plate')
    elif sort_by == 'newest':
        vendors = vendors.order_by('-created_at')
    else:
        vendors = vendors.order_by('-created_at') # Default sorting

    # Pagination
    paginator = Paginator(vendors, 6) # 6 vendors per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get distinct cities and categories for filters
    cities = VendorProfile.objects.filter(is_verified=True).values_list('service_area', flat=True).distinct()
    categories_filter = MenuCategory.objects.all().distinct('name') # Depending on DB, distinct by field might not work in SQLite, but usually works fine or we can just get values

    context = {
        'page_obj': page_obj,
        'cities': cities,
        'categories_filter': MenuCategory.objects.values('id', 'name').distinct(),
        'request_GET': request.GET, # pass GET parameters to maintain filter state in pagination
    }
    return render(request, 'marketplace/caterer_list.html', context)


def caterer_detail(request, id, slug):
    # Get verified vendor by ID
    vendor = get_object_or_404(VendorProfile, id=id, is_verified=True)
    
    # Prefetch categories along with their *available* menu items
    available_items_prefetch = Prefetch(
        'items',
        queryset=MenuItem.objects.filter(is_available=True),
        to_attr='available_items'
    )
    categories = vendor.categories.prefetch_related(available_items_prefetch).all()
    
    context = {
        'vendor': vendor,
        'categories': categories,
    }
    return render(request, 'marketplace/caterer_detail.html', context)
