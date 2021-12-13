from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('parkings', views.ParkingPlacesList.as_view(), name='parkingplaces_list'),
    path('reserve', views.index, name='reserve'),
]