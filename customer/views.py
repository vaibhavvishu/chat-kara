from django.shortcuts import render
from accounts.decorators import role_required
from django.contrib.auth.decorators import login_required
from booking.models import Booking
from vendor.models import Review

@login_required
@role_required(allowed_roles=['Customer'])
def dashboard(request):
    bookings_count = Booking.objects.filter(customer=request.user).count()
    user_reviews = Review.objects.filter(customer=request.user)
    
    context = {
        'bookings_count': bookings_count,
        'user_reviews': user_reviews,
        'reviews_count': user_reviews.count()
    }
    return render(request, 'customer/dashboard.html', context)
