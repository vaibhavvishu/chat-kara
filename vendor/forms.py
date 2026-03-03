from django import forms
from .models import VendorProfile, MenuCategory, MenuItem

class VendorProfileForm(forms.ModelForm):
    class Meta:
        model = VendorProfile
        fields = ['business_name', 'business_description', 'service_area', 'address', 
                  'starting_price_per_plate', 'profile_image', 'cover_image']
        widgets = {
            'business_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your business name'}),
            'business_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your services...'}),
            'service_area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Mumbai, Delhi'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full address'}),
            'starting_price_per_plate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 500'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class MenuCategoryForm(forms.ModelForm):
    class Meta:
        model = MenuCategory
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Starters, Main Course'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional description'}),
        }

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['category', 'name', 'description', 'price_per_plate', 'image', 'is_available']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Paneer Tikka'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price_per_plate': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, vendor=None, *args, **kwargs):
        super(MenuItemForm, self).__init__(*args, **kwargs)
        if vendor:
            self.fields['category'].queryset = MenuCategory.objects.filter(vendor=vendor)
