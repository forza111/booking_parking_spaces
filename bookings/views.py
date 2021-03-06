from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages

from .models import ParkingPlaces, Bookings


class ParkingPlacesList(ListView):
    model = ParkingPlaces


class ParkingPlacesDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'bookings.delete_parkingplaces'
    model = ParkingPlaces
    template_name = 'bookings/parkingplaces_delete.html'
    success_url = reverse_lazy('parking')


class CreateParkingPlaces(PermissionRequiredMixin, CreateView):
    permission_required = 'bookings.add_parkingplaces'
    model = ParkingPlaces
    template_name = 'bookings/parking_places_create.html'
    fields = ["parking_number"]


class CreateBooking(PermissionRequiredMixin, CreateView):
    permission_required = 'bookings.add_bookings'
    model = Bookings
    template_name = 'bookings/booking_create.html'
    fields = ["user_id", "park_num", "start_date", "end_date"]
    error_message = {"date_is_busy": "Место уже забронировано на это время",
                     "invalid_date": "Дата окончания бронирования не может быть раньше даты начала."}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['park_num'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        try:
            return super(CreateBooking, self).form_valid(form)
        except IntegrityError:
            messages.error(self.request, self.error_message["invalid_date"])
            return self.form_invalid(form)
        except ValueError:
            messages.error(self.request, self.error_message["date_is_busy"])
            return self.form_invalid(form)


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