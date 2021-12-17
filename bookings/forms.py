from .models import Bookings
from django.forms import ModelForm, DateTimeInput, NumberInput, TextInput


class BookingsForm(ModelForm):
    class Meta:
        model = Bookings
        fields = ["user_id","park_num", "start_date", "end_date"]