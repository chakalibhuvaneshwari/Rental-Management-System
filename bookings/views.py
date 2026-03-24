from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from properties.models import Property

@login_required
def book_property(request, property_id):
    if request.user.role != 'TENANT':
        messages.error(request, "Only tenants can book properties.")
        return redirect('property_detail', pk=property_id)
        
    prop = get_object_or_404(Property, pk=property_id)
    if request.method == 'POST':
        # Check if already requested
        if Booking.objects.filter(property=prop, tenant=request.user, status__in=['PENDING', 'ACCEPTED']).exists():
            messages.warning(request, "You have already requested this property.")
        else:
            Booking.objects.create(property=prop, tenant=request.user)
            messages.success(request, "Booking request sent successfully to the owner!")
    return redirect('property_detail', pk=property_id)

@login_required
def my_requests(request):
    if request.user.role != 'TENANT':
        return redirect('home')
    bookings = Booking.objects.filter(tenant=request.user).order_by('-created_at')
    return render(request, 'bookings/my_requests.html', {'bookings': bookings})

@login_required
def manage_bookings(request):
    if request.user.role != 'OWNER':
        return redirect('home')
    # Get bookings for properties owned by this user
    bookings = Booking.objects.filter(property__owner=request.user).order_by('-created_at')
    return render(request, 'bookings/manage.html', {'bookings': bookings})

@login_required
def update_booking(request, booking_id, action):
    if request.user.role != 'OWNER':
        return redirect('home')
    
    booking = get_object_or_404(Booking, pk=booking_id, property__owner=request.user)
    if action == 'accept':
        booking.status = 'ACCEPTED'
        # Can optionally set property to not available
        prop = booking.property
        prop.is_available = False
        prop.save()
        messages.success(request, f"Accepted booking request for {booking.property.title}.")
    elif action == 'reject':
        booking.status = 'REJECTED'
        messages.success(request, f"Rejected booking request for {booking.property.title}.")
        
    booking.save()
    return redirect('manage_bookings')

@login_required
def payment_checkout(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, tenant=request.user, status='ACCEPTED')
    if booking.is_paid:
        messages.info(request, "This booking has already been paid for.")
        return redirect('my_requests')
        
    return render(request, 'bookings/checkout.html', {'booking': booking})

@login_required
def process_payment(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id, tenant=request.user, status='ACCEPTED')
        booking.is_paid = True
        booking.save()
        messages.success(request, f"Payment of ₹{booking.property.deposit} successful! Your receipt has been generated.")
        return redirect('my_requests')
    return redirect('home')
