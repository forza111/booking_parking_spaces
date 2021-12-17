from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('parking', views.ParkingPlacesList.as_view(), name='parking'),
    path('parking/<str:pk>/delete', views.ParkingPlacesDeleteView.as_view(), name='delete_parking_places'),
    path('parking/create', views.CreateParkingPlaces.as_view(), name='create_parking_places'),

    path('reserve/<str:pk>', views.reserve, name='reserve'),
    path('bookings/<str:pk>/list', views.BookingsList.as_view(), name='bookings_list'),
    path('booking/<int:pk>/delete', views.BookingDelete.as_view(), name='delete_booking'),
    path('booking/<int:pk>/update', views.BookingUpdate.as_view(), name='update_booking'),

    # path('reserve/<str:pk>', views.BookingsCreateView.as_view(), name='reserve'),

]