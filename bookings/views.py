import datetime

from django.http import HttpResponse
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import ParkingPlaces, Bookings
from .forms import BookingsForm


class ParkingPlacesList(ListView):
    model = ParkingPlaces


class ParkingPlacesDeleteView(PermissionRequiredMixin,DeleteView):
    permission_required = 'bookings.delete_parkingplaces'
    model = ParkingPlaces
    template_name = 'bookings/parkingplaces_delete.html'
    success_url = reverse_lazy('parking')


class CreateParkingPlaces(PermissionRequiredMixin,CreateView):
    permission_required = 'bookings.add_parkingplaces'
    model = ParkingPlaces
    template_name = 'bookings/parking_places_create.html'
    fields = ["parking_number"]


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


class BookingsList(PermissionRequiredMixin, ListView):
    permission_required = 'bookings.view_bookings'
    model = Bookings
    template_name = "bookings/bookings_list.html"

    def get_queryset(self):
        return Bookings.objects.filter(park_num=self.kwargs['pk'])


class BookingDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'bookings.delete_bookings'
    model = Bookings
    template_name = 'bookings/booking_delete.html'

    def get_success_url(self):
        return reverse_lazy('bookings_list', kwargs={'pk': self.object.park_num})


class BookingUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'bookings.change_bookings'
    model = Bookings
    template_name = 'bookings/booking_update.html'
    fields = ["start_date", "end_date"]

    def get_success_url(self):
        return reverse_lazy('bookings_list', kwargs={'pk': self.object.park_num})