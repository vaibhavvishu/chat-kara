from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Prefetch, Q, Avg
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from vendor.models import VendorProfile, MenuCategory, MenuItem, Review
from .forms import ReviewForm

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
        try:
            budget_val = float(budget)
            min_budget = max(0, budget_val - 100)
            max_budget = budget_val + 100
            vendors = vendors.filter(starting_price_per_plate__gte=min_budget, starting_price_per_plate__lte=max_budget)
        except ValueError:
            pass
        
    category_id = request.GET.get('category')
    if category_id:
        vendors = vendors.filter(categories__id=category_id).distinct()

    event_type = request.GET.get('event_type')
    if event_type:
        vendors = vendors.filter(
            Q(business_description__icontains=event_type) |
            Q(categories__name__icontains=event_type)
        ).distinct()

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
    
    # Reviews
    reviews = vendor.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    form = ReviewForm()

    context = {
        'vendor': vendor,
        'categories': categories,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'review_form': form,
    }
    return render(request, 'marketplace/caterer_detail.html', context)

@login_required
def submit_review(request, vendor_id):
    vendor = get_object_or_404(VendorProfile, id=vendor_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Check if user already reviewed
            if Review.objects.filter(vendor=vendor, customer=request.user).exists():
                messages.error(request, 'You have already reviewed this caterer.')
            else:
                review = form.save(commit=False)
                review.vendor = vendor
                review.customer = request.user
                review.save()
                messages.success(request, 'Your review has been posted successfully.')
        else:
            messages.error(request, 'Failed to submit review. Make sure all fields are valid.')
    return redirect('caterer_detail', id=vendor.id, slug=slugify(vendor.business_name))
