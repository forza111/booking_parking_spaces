import math

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db.models import Q, F
from django.core.validators import MaxValueValidator
import datetime


class ParkingPlaces(models.Model):
    parking_number = models.CharField("Номер парковочного места", max_length=20, primary_key=True)

    def __str__(self):
        return self.parking_number

    def get_absolute_url(self):
        return reverse('parking')


class Bookings(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    park_num = models.ForeignKey(ParkingPlaces, on_delete=models.CASCADE, verbose_name="Номер парковочного места")
    start_date = models.DateTimeField("Дата начала бронирования")
    end_date = models.DateTimeField("Дата окончания бронирования")
    hours = models.PositiveSmallIntegerField("Количество часов")

    def __str__(self):
        return self.park_num

    def get_absolute_url(self):
        return reverse('parking')

    class Meta:
        constraints = [models.CheckConstraint(check=Q(end_date__gt=F('start_date')), name='date_field_check')]


@receiver(pre_save, sender=Bookings)
def check_booking_date(sender, instance, **kwargs):
    if Bookings.objects.all().filter(
            park_num=instance.park_num, start_date__lte=instance.end_date,end_date__gte=instance.start_date):
        raise ValueError


@receiver(pre_save, sender=Bookings)
def create_booking_hours(sender, instance, **kwargs):
    bookings_hours = math.ceil((instance.end_date - instance.start_date).total_seconds()/3600)
    instance.hours = bookings_hours