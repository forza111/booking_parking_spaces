from django.db import models
from django.contrib.auth.models import User

class ParkingPlaces(models.Model):
    parking_number = models.CharField("Номер парковочного места", max_length=20, primary_key=True)

    def __str__(self):
        return self.parking_number


class Bookings(models.Model):
    parking_number = models.CharField("Номер парковочного места", max_length=20, primary_key=True)

    def __str__(self):
        return self.parking_number