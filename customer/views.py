from django.shortcuts import render
from accounts.decorators import role_required
from django.contrib.auth.decorators import login_required
from booking.models import Booking

@login_required
@role_required(allowed_roles=['Customer'])
def dashboard(request):
    bookings_count = Booking.objects.filter(customer=request.user).count()
    return render(request, 'customer/dashboard.html', {'bookings_count': bookings_count})
