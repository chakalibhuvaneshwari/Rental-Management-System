from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                # Role-based redirect
                if user.role == 'OWNER':
                    return redirect('owner_dashboard')
                elif user.role == 'ADMIN':
                    return redirect('admin_dashboard')
                else:
                    return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        # Custom registration logic to handle role
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role', 'TENANT')
        phone_number = request.POST.get('phone_number')
        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')
            
        user = CustomUser.objects.create_user(username=username, email=email, password=password, role=role, phone_number=phone_number)
        login(request, user)
        messages.success(request, "Registration successful!")
        if role == 'OWNER':
            return redirect('owner_dashboard')
        return redirect('home')
    return render(request, 'users/register.html')

from django.shortcuts import get_object_or_404
from .models import Wishlist, Message
from properties.models import Property

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).order_by('-added_at')
    return render(request, 'users/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def toggle_wishlist(request, property_id):
    if request.method == 'POST':
        prop = get_object_or_404(Property, pk=property_id)
        wishlist_item = Wishlist.objects.filter(user=request.user, property=prop).first()
        if wishlist_item:
            wishlist_item.delete()
            messages.success(request, "Removed from wishlist.")
        else:
            Wishlist.objects.create(user=request.user, property=prop)
            messages.success(request, "Added to wishlist!")
    return redirect('property_detail', pk=property_id)

@login_required
def messages_view(request):
    # Group messages by the 'other' user to form conversations
    from django.db.models import Q, Max
    user = request.user
    
    # Get all users we have exchanged messages with, alongside the latest message time
    conversations = []
    contact_ids = set()
    
    all_msgs = Message.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('-timestamp')
    for msg in all_msgs:
        other_user = msg.sender if msg.receiver == user else msg.receiver
        if other_user.id not in contact_ids:
            contact_ids.add(other_user.id)
            conversations.append({
                'contact': other_user,
                'latest_message': msg,
            })
            
    return render(request, 'users/messages.html', {'conversations': conversations})

@login_required
def message_thread(request, user_id):
    from django.db.models import Q
    other_user = get_object_or_404(CustomUser, pk=user_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content
            )
            return redirect('message_thread', user_id=user_id)
            
    messages_list = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')
    
    return render(request, 'users/message_thread.html', {'messages_list': messages_list, 'other_user': other_user})

@login_required
def admin_dashboard(request):
    if request.user.role != 'ADMIN':
        messages.error(request, "Access denied. Admins only.")
        return redirect('home')
        
    from properties.models import Property
    from bookings.models import Booking
    
    context = {
        'total_users': CustomUser.objects.count(),
        'total_properties': Property.objects.count(),
        'total_bookings': Booking.objects.count(),
        'recent_users': CustomUser.objects.order_by('-date_joined')[:5],
        'recent_properties': Property.objects.order_by('-created_at')[:5],
    }
    return render(request, 'users/admin_dashboard.html', context)

@login_required
def send_message(request, property_id):
    if request.method == 'POST':
        prop = get_object_or_404(Property, pk=property_id)
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                sender=request.user,
                receiver=prop.owner,
                property=prop,
                content=content
            )
            messages.success(request, "Message sent to owner!")
    return redirect('property_detail', pk=property_id)
