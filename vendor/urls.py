from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='vendor_dashboard'),
    path('profile/', views.vendor_profile, name='vendor_profile'),
    path('menu/', views.manage_menu, name='manage_menu'),
    path('menu/add-category/', views.add_category, name='add_category'),
    path('menu/add-item/', views.add_item, name='add_item'),
    path('menu/delete-item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('menu/toggle-item/<int:item_id>/', views.toggle_item_availability, name='toggle_item_availability'),
]
