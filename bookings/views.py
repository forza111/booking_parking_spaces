from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import ParkingPlaces


def index(request):
    return HttpResponse("Hello, world")


class ParkingPlacesList(ListView):
    model = ParkingPlaces
    queryset = ParkingPlaces.objects.all()

