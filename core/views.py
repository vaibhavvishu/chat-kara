from django.shortcuts import render
from django.db.models import Q
from vendor.models import VendorProfile

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')
