from .models import Bookings
from django.forms import ModelForm, DateTimeInput, NumberInput, TextInput


class BookingsForm(ModelForm):
    class Meta:
        model = Bookings
        fields = ["user_id","park_num", "start_date", "end_date", "hours"]

        # widgets = {
        #     "user_id": NumberInput(attrs={
        #         'class': 'form-control',
        #         'placeholder': "id пользователя"
        #     }),
        #     "park_num": TextInput(attrs={
        #         'class': 'form-control',
        #         'placeholder': "Номер парковочного места"
        #     }),
        #     "start_date": DateTimeInput(attrs={
        #         'class': 'form-control',
        #         'placeholder': "Начало бронирования"
        #     }),
        #     "end_date": DateTimeInput(attrs={
        #         'class': 'form-control',
        #         'placeholder': "Окончание бронирования"
        #     }),
        #     "hours": NumberInput(attrs={
        #         'class': 'form-control',
        #         'placeholder': "Количество часов"
        #     }),
        # }