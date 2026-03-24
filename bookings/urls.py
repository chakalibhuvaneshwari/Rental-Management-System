from django.urls import path
from . import views

urlpatterns = [
    path('request/<int:property_id>/', views.book_property, name='book_property'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('manage/', views.manage_bookings, name='manage_bookings'),
    path('update/<int:booking_id>/<str:action>/', views.update_booking, name='update_booking'),
    path('checkout/<int:booking_id>/', views.payment_checkout, name='payment_checkout'),
    path('checkout/process/<int:booking_id>/', views.process_payment, name='process_payment'),
]
