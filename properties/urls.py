from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('owner/dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('owner/add/', views.add_property, name='add_property'),
]
