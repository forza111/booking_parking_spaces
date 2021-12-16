import datetime

from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.shortcuts import render

from .models import ParkingPlaces
from .forms import BookingsForm


def index(request):
    return HttpResponse("Hello, world")

class ParkingPlacesList(ListView):
    model = ParkingPlaces
    queryset = ParkingPlaces.objects.all()

def reserve(request, pk):
    error = ''
    if request.method == 'POST':
        form = BookingsForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.user_id = request.user.id
            form.park_num = pk
            form.save()
        else:
            error = "форма не верна"

    form = BookingsForm()
    data = {
        'form': form,
        'error': error,
        'pk': pk
    }
    return render(request, "bookings/reservation.html", data)

