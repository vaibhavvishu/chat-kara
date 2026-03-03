from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Booking
from .forms import BookingForm
from vendor.models import VendorProfile

def is_customer(user):
    return user.is_authenticated and user.role == 'Customer'

def is_vendor(user):
    return user.is_authenticated and user.role == 'Vendor'

@login_required
@user_passes_test(is_customer, login_url='home')
def create_booking(request, vendor_id):
    vendor = get_object_or_404(VendorProfile, id=vendor_id, is_verified=True)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.vendor = vendor
            booking.save()
            messages.success(request, f"Your booking request has been sent to {vendor.business_name} successfully!")
            return redirect('customer_booking_history')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookingForm()
        
    context = {
        'form': form,
        'vendor': vendor,
    }
    return render(request, 'booking/booking_form.html', context)

@login_required
@user_passes_test(is_customer, login_url='home')
def customer_booking_history(request):
    bookings = Booking.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'booking/customer_bookings.html', {'bookings': bookings})

@login_required
@user_passes_test(is_customer, login_url='home')
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user, status='Pending')
    if request.method == 'POST':
        booking.status = 'Cancelled'
        booking.save()
        messages.success(request, "Booking has been cancelled.")
    return redirect('customer_booking_history')

@login_required
@user_passes_test(is_vendor, login_url='home')
def vendor_booking_requests(request):
    vendor_profile = get_object_or_404(VendorProfile, user=request.user)
    bookings = Booking.objects.filter(vendor=vendor_profile).order_by('-created_at')
    return render(request, 'booking/vendor_bookings.html', {'bookings': bookings})

@login_required
@user_passes_test(is_vendor, login_url='home')
def update_booking_status(request, booking_id):
    vendor_profile = get_object_or_404(VendorProfile, user=request.user)
    booking = get_object_or_404(Booking, id=booking_id, vendor=vendor_profile)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Booking.STATUS_CHOICES).keys():
            booking.status = new_status
            booking.save()
            messages.success(request, f"Booking #{booking.id} marked as {new_status}.")
        else:
            messages.error(request, "Invalid status.")
            
    return redirect('vendor_booking_requests')
