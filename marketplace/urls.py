from django.urls import path
from . import views

urlpatterns = [
    path('caterers/', views.caterer_list, name='caterer_list'),
    path('caterer/<int:id>/<slug:slug>/', views.caterer_detail, name='caterer_detail'),
    path('caterer/<int:vendor_id>/review/', views.submit_review, name='submit_review'),
]
