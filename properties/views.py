import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import Property

def parse_smart_search(query):
    """
    Parses natural language query to return Q objects.
    e.g., '2BHK under 8000 in Hyderabad sharing for 3'
    """
    search_q = Q()
    query = query.lower()
    
    # Process 'under X' or '< X'
    price_match = re.search(r'under\s+(\d+)|<\s*(\d+)', query)
    if price_match:
        price = price_match.group(1) or price_match.group(2)
        search_q &= Q(price__lte=int(price))
        
    # Process BHK
    bhk_match = re.search(r'(\d)bhk', query)
    if bhk_match:
        bhk = f"{bhk_match.group(1)}BHK"
        search_q &= Q(property_type=bhk)
        
    # Process city/location (rudimentary)
    cities = ['hyderabad', 'bangalore', 'mumbai', 'delhi', 'chennai', 'pune']
    for city in cities:
        if city in query:
            search_q &= Q(city__icontains=city)
            break
            
    # Process sharing
    if 'sharing' in query:
        search_q &= Q(room_type='SHARING')
        cap_match = re.search(r'for\s+(\d)', query)
        if cap_match:
            search_q &= Q(sharing_capacity__gte=int(cap_match.group(1)))
            
    return search_q

def home_view(request):
    query = request.GET.get('q', '')
    if query:
        search_q = parse_smart_search(query)
        # Add basic text search fallback
        search_q |= Q(title__icontains=query) | Q(location__icontains=query)
        properties = Property.objects.filter(search_q, is_available=True)
    else:
        properties = Property.objects.filter(is_available=True).order_by('-created_at')[:6]
        
    context = {
        'properties': properties,
        'query': query,
    }
    return render(request, 'properties/home.html', context)

def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    # Similar properties (same city and type)
    similar = Property.objects.filter(city=property_obj.city, property_type=property_obj.property_type).exclude(pk=pk)[:3]
    return render(request, 'properties/detail.html', {'property': property_obj, 'similar': similar})

@login_required
def owner_dashboard(request):
    if request.user.role != 'OWNER':
        messages.error(request, "Access denied.")
        return redirect('home')
    properties = Property.objects.filter(owner=request.user)
    return render(request, 'properties/owner_dashboard.html', {'properties': properties})

@login_required
def add_property(request):
    if request.user.role != 'OWNER':
        messages.error(request, "Only owners can add properties.")
        return redirect('home')
        
    if request.method == 'POST':
        # Processing form manually for simplicity
        Property.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            city=request.POST.get('city'),
            location=request.POST.get('location'),
            price=request.POST.get('price'),
            deposit=request.POST.get('deposit'),
            property_type=request.POST.get('property_type'),
            room_type=request.POST.get('room_type'),
            sharing_capacity=request.POST.get('sharing_capacity', 1),
            amenities=request.POST.get('amenities'),
            latitude=request.POST.get('latitude') or None,
            longitude=request.POST.get('longitude') or None,
            owner=request.user
        )
        messages.success(request, "Property added successfully!")
        return redirect('owner_dashboard')
        
    return render(request, 'properties/add_property.html')
