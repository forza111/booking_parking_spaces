import datetime

from django.http import HttpResponse
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.shortcuts import render
from django.urls import reverse_lazy

from .models import ParkingPlaces, Bookings
from .forms import BookingsForm


def index(request):
    return HttpResponse("Hello, world")


class ParkingPlacesList(ListView):
    model = ParkingPlaces


class ParkingPlacesDeleteView(DeleteView):
    model = ParkingPlaces
    template_name = 'bookings/parkingplaces_delete.html'
    success_url = reverse_lazy('parking')


class CreateParkingPlaces(CreateView):
    model = ParkingPlaces
    template_name = 'bookings/parking_places_create.html'
    fields = ["parking_number"]

# class BookingsCreateView(CreateView, DetailView):
#     model = Bookings
#     template_name = "bookings/reservation.html"
#     fields = ["user_id", "park_num", "start_date", "end_date", "hours"]


def reserve(request, pk):
    error = ''
    if request.method == 'POST':
        form = BookingsForm(request.POST)
        if form.is_valid():
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

