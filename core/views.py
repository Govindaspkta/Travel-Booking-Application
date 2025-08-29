from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import  messages
from django.db.models import Q
from datetime import datetime
from .forms import RegistrationForm, ProfileForm, BookingForm, TravelOptionFilterForm
from .models import TravelOption, Booking

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

def home(request):
    form = TravelOptionFilterForm(request.GET)
    options = TravelOption.objects.all()
    if form.is_valid():
        type = form.cleaned_data['type']
        source = form.cleaned_data['source']
        destination = form.cleaned_data['destination']
        date = form.cleaned_data['date']
        query = Q()
        if type:
            query &= Q(type=type)
        if source:
            query &= Q(source__icontains=source)
        if destination:
            query &= Q(destination__icontains=destination)
        if date:
            query &= Q(date_time__date=date)
        options = options.filter(query)
    return render(request, 'home.html', {'options': options, 'form': form})

@login_required
def book(request, option_id):
    option = get_object_or_404(TravelOption, id=option_id)
    if request.method == 'POST':
        form = BookingForm(request.POST, travel_option=option)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.travel_option = option
            booking.save()
            #debg
            print("booking saved",booking.id)
            messages.success(request,"🎉 Booking Successful!")
            return redirect('bookings')
        else:
            print("form errors",form.errors)
    else:
      
        form = BookingForm(travel_option=option)
    return render(request, 'book.html', {'form': form, 'option': option})

@login_required
def bookings(request):
    now = datetime.now()
    current_bookings = Booking.objects.filter(user=request.user, status='confirmed', travel_option__date_time__gte=now)
    past_bookings = Booking.objects.filter(user=request.user).exclude(id__in=[b.id for b in current_bookings])
    return render(request, 'bookings.html', {'current_bookings': current_bookings, 'past_bookings': past_bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status == 'confirmed':
        booking.status = 'cancelled'
        booking.travel_option.available_seats += booking.number_of_seats
        booking.travel_option.save()
        booking.save()
    return redirect('bookings')