from django.shortcuts import render, redirect
from location.models import *
from django.shortcuts import get_object_or_404
from location.models import *
from django.contrib.auth.decorators import login_required
from .forms import *
import folium, geocoder
from geopy.geocoders import Nominatim
from django.db.models import Q
from profiles.models import ProfilePhoto

# Create your views here.
def index(request):
    profile_photo = None
    locations = list(Location.objects.all().values('name', 'category', 'latitude', 'longitude', 'image'))
    categories = Category.objects.all()
    if request.user.is_authenticated:
        try:
            profile_photo = ProfilePhoto.objects.get(username=request.user)
        except ProfilePhoto.DoesNotExist:
            pass
    search_query, heading = None, 'Explore Makerere University'
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            location = geocoder.osm(search_query)
            if location:
                latitude = location.lat
                longitude = location.lng
                heading = f'{search_query} at {latitude:.6f}, {longitude:.2f}'
                map = folium.Map(
                    location=[latitude, longitude],
                    zoom_start=17
                )
                folium.Marker(
                        [latitude, longitude],
                        tooltip=search_query,
                        popup=f'{search_query}\n{latitude}, {longitude}\n{location.country}'
                    ).add_to(map)
                map = map._repr_html_()
                return render(request, 'core/index.html', {
                    'categories' : categories,
                    "form" : form,
                    'heading' : heading,
                    'search_query' : search_query,
                    'map' : map,
                    'profile_photo' : profile_photo
                })
    else:
        form = SearchForm(initial={'search_query': search_query})
    return render(request, 'core/index.html', {
        'categories' : categories,
        "form" : form,
        'favorites_json' : locations,
        'heading' : heading,
        'profile_photo' : profile_photo
    })


def directions(request):
    navigation, heading, profile_photo = None, None, None
    if request.user.is_authenticated:
        try:
            profile_photo = ProfilePhoto.objects.get(username=request.user)
        except ProfilePhoto.DoesNotExist:
            pass
    if request.method == 'POST':
        form = NavigationForm(request.POST)
        if form.is_valid():
            source = form.cleaned_data['source']
            destination = form.cleaned_data['destination']
            geolocator = Nominatim(user_agent="my_geocoder")
            source_location = geolocator.geocode(source)
            destination_location = geolocator.geocode(destination)
            if source_location and destination_location:
                heading = f'Navigating from {source} to {destination}'
                navigation = [{
                    'source' : source,
                    'source_latitude' : source_location.latitude,
                    'source_longitude' : source_location.longitude,
                    'destination' : destination,
                    'destination_latitude' : destination_location.latitude,
                    'destination_longitude' : destination_location.longitude 
                }]
                if request.user.is_authenticated:
                    na_category, _ = Category.objects.get_or_create(name='Unspecified')
                    start_location_obj, _ = Location.objects.get_or_create(name=source, defaults={
                        'category': na_category,
                        'latitude': source_location.latitude,
                        'longitude': source_location.longitude,
                        'created_by': request.user
                    })
                    
                    end_location_obj, _ = Location.objects.get_or_create(name=destination, defaults={
                        'category': na_category,
                        'latitude': destination_location.latitude,
                        'longitude': destination_location.longitude,
                        'created_by': request.user
                    })

                    # Create a Navigation object and save it to the database
                    if request.user.is_authenticated:
                        new_navigation = Navigation(
                            start=start_location_obj,
                            destination=end_location_obj,
                            created_by=request.user
                        )
                        new_navigation.save()
    else:
        form = NavigationForm()
    navigation_history = None
    if request.user.is_authenticated:
        navigation_history = Navigation.objects.filter(created_by=request.user)
    return render(request, 'core/directions.html', {
        'logged_in' : request.user.is_authenticated,
        'navigation' : navigation,
        'heading' : heading,
        'form' : form,
        'navigation_history' : navigation_history,
        'profile_photo' : profile_photo
    })

@login_required(login_url='login')
def contribute(request):
    try:
        profile_photo = ProfilePhoto.objects.get(username=request.user)
    except ProfilePhoto.DoesNotExist:
        profile_photo = None
    return render(request, 'core/contribute.html', {
        'profile_photo' : profile_photo
    })

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
        form = RegistrationForm()
    return render(request, 'core/register.html', {
        'form' : form
    })

def login(request):
    return render(request, 'core/login.html')

def favorites(request):
    profile_photo = None
    # Define latitude and longitude bounds
    min_latitude = 0.327804
    max_latitude = 0.33984
    min_longitude = 32.563417
    max_longitude = 32.573234

    # Create Q objects to define the filtering conditions
    latitude_condition = Q(latitude__gte=min_latitude, latitude__lte=max_latitude)
    longitude_condition = Q(longitude__gte=min_longitude, longitude__lte=max_longitude)

    # Combine the Q objects using logical AND
    combined_condition = latitude_condition & longitude_condition

    # Filter locations based on the combined condition
    locations = Location.objects.filter(combined_condition)[:12]
    categories = Category.objects.all()

    if request.user.is_authenticated:
        try:
            profile_photo = ProfilePhoto.objects.get(username=request.user)
        except ProfilePhoto.DoesNotExist:
            pass
    return render(request, 'core/favorites.html', {
        'locations' : locations,
        'categories' : categories,
        'profile_photo' : profile_photo
    })

@login_required
def delete_account(request):
    user = request.user
    user.delete()
    return redirect('/')

@login_required
def edit(request):
    if request.method == 'POST':
        form = EditAccountForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            uploaded_image = form.cleaned_data['photo']
            if uploaded_image:
                # Create and save the ProfilePhoto instance
                profile_photo = ProfilePhoto(image=uploaded_image, username=request.user)
                profile_photo.save()
            data_to_pass = {'success': True}
            return redirect('/profile/', **data_to_pass)
    else:
        form = EditAccountForm(instance=request.user)
    try:
        profile_photo = ProfilePhoto.objects.get(username=request.user)
    except ProfilePhoto.DoesNotExist:
        profile_photo = None
    return render(request, 'core/edit.html', {
        'form' : form,
        'profile_photo' : profile_photo
    })