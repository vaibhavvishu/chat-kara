from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.decorators import role_required
from django.contrib.auth.decorators import login_required
from .models import VendorProfile, MenuCategory, MenuItem
from .forms import VendorProfileForm, MenuCategoryForm, MenuItemForm
from booking.models import Booking

@login_required
@role_required(allowed_roles=['Vendor'])
def dashboard(request):
    try:
        profile = request.user.vendor_profile
        menu_items_count = profile.menu_items.count()
        categories_count = profile.categories.count()
        bookings_count = Booking.objects.filter(vendor=profile).count()
    except VendorProfile.DoesNotExist:
        menu_items_count = 0
        categories_count = 0
        bookings_count = 0
        messages.warning(request, "Please create your vendor profile first.")
        return redirect('vendor_profile')
        
    context = {
        'menu_items_count': menu_items_count,
        'categories_count': categories_count,
        'bookings_count': bookings_count,
        'profile': profile,
    }
    return render(request, 'vendor/dashboard.html', context)

@login_required
@role_required(allowed_roles=['Vendor'])
def vendor_profile(request):
    try:
        profile = request.user.vendor_profile
    except VendorProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = VendorProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_profile = form.save(commit=False)
            new_profile.user = request.user
            new_profile.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('vendor_dashboard')
    else:
        form = VendorProfileForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'vendor/profile.html', context)

@login_required
@role_required(allowed_roles=['Vendor'])
def manage_menu(request):
    try:
        profile = request.user.vendor_profile
    except VendorProfile.DoesNotExist:
        messages.warning(request, "Please create your profile before managing the menu.")
        return redirect('vendor_profile')

    categories = profile.categories.prefetch_related('items').all()
    
    category_form = MenuCategoryForm()
    item_form = MenuItemForm(vendor=profile)

    context = {
        'categories': categories,
        'category_form': category_form,
        'item_form': item_form,
        'profile': profile,
    }
    return render(request, 'vendor/menu_management.html', context)

@login_required
@role_required(allowed_roles=['Vendor'])
def add_category(request):
    if request.method == 'POST':
        form = MenuCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.vendor = request.user.vendor_profile
            category.save()
            messages.success(request, "Category added successfully.")
        else:
            messages.error(request, "Failed to add category. Please check the form.")
    return redirect('manage_menu')

@login_required
@role_required(allowed_roles=['Vendor'])
def add_item(request):
    if request.method == 'POST':
        profile = request.user.vendor_profile
        form = MenuItemForm(profile, request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.vendor = profile
            item.save()
            messages.success(request, "Menu item added successfully.")
        else:
            messages.error(request, "Failed to add menu item. Please check the form.")
    return redirect('manage_menu')

@login_required
@role_required(allowed_roles=['Vendor'])
def delete_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id, vendor=request.user.vendor_profile)
    item.delete()
    messages.success(request, "Menu item deleted.")
    return redirect('manage_menu')

@login_required
@role_required(allowed_roles=['Vendor'])
def toggle_item_availability(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id, vendor=request.user.vendor_profile)
    item.is_available = not item.is_available
    item.save()
    messages.success(request, f"'{item.name}' availability updated.")
    return redirect('manage_menu')
