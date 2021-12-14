from .models import Bookings
from django.forms import ModelForm, DateTimeInput, NumberInput


class BookingsForm(ModelForm):
    class Meta:
        model = Bookings
        fields = ["start_date", "hours"]

        widgets = {
            "start_date": DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': "Начало бронирования"
            }),
            "hours": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': "Количество часов"
            }),
        }