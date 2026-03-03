from django.urls import path
from . import views

urlpatterns = [
    path('caterers/', views.caterer_list, name='caterer_list'),
    path('caterer/<int:id>/<slug:slug>/', views.caterer_detail, name='caterer_detail'),
]
