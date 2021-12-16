from django.db import models
from django.contrib.auth.models import User

class ParkingPlaces(models.Model):
    parking_number = models.CharField("Номер парковочного места", max_length=20, primary_key=True)

    def __str__(self):
        return self.parking_number


class Bookings(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    park_num = models.ForeignKey(ParkingPlaces, on_delete=models.CASCADE, verbose_name="Номер парковочного места")
    start_date = models.DateTimeField("Дата начала бронирования")
    end_date = models.DateTimeField("Дата окончания бронирования")
    hours = models.PositiveSmallIntegerField("Количество часов")


    def __str__(self):
        return self.park_num