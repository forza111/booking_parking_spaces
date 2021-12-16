from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('parking', views.ParkingPlacesList.as_view(), name='parking'),
    path('parking/<str:pk>/delete', views.ParkingPlacesDeleteView.as_view(), name='delete_parking_places'),
    path('parking/create', views.CreateParkingPlaces.as_view(), name='create_parking_places'),

    path('reserve/<str:pk>', views.reserve, name='reserve'),
    # path('reserve/<str:pk>', views.BookingsCreateView.as_view(), name='reserve'),

]