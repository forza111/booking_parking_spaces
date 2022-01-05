from datetime import datetime
from datetime import timedelta

from django.contrib.auth.models import User,Permission
from django.db.models import Q
import pytest

from bookings.models import ParkingPlaces, Bookings


current_time = datetime.now()
past_time = [current_time - timedelta(hours=x) for x in range(1,11)]
future_time = [current_time + timedelta(hours=x) for x in range(1,11)]

database = {
    "parking_number": ["A1", "A2"],
    "create_parking_number":
        {
            "parking_number": "A3",
        },
    "booking":
        {
            "exist_booking":
                {
                "park_num": "A1",
                'start_date': future_time[4],
                "end_date": future_time[5]
                },
            "update_booking":
                {
                    "park_num": "A1",
                    'start_date': future_time[6],
                    "end_date": future_time[8]
                },
            "normal_booking_1":
                {
                "park_num": "A1",
                'start_date': future_time[1],
                "end_date": future_time[2]
                },
            "broken_booking_1":
                {
                    "park_num": "A1",
                    'start_date': future_time[1],
                    "end_date": future_time[5]
                },
            "broken_booking_2":
                {
                    "park_num": "A1",
                    'start_date': future_time[4],
                    "end_date": future_time[7]
                },
        },
}


@pytest.fixture
def create_user_employee(db):
    user = User.objects.create_user('maksim', 'maksim@example.com', 'passwordmaksim')
    manager_permissions = Permission.objects.filter(Q(codename="add_bookings") | Q(codename="view_bookings"))
    user.user_permissions.add(*manager_permissions)
    return user

@pytest.fixture
def create_user_manager(db):
    user = User.objects.create_user('nikita', 'nikita@example.com', 'passwordnikita')
    manager_permissions = Permission.objects.filter(
        Q(codename="add_parkingplaces") |
        Q(codename="delete_parkingplaces") |
        Q(codename="add_bookings") |
        Q(codename="view_bookings") |
        Q(codename="delete_bookings") |
        Q(codename="change_bookings")
    )
    user.user_permissions.add(*manager_permissions)
    return user

@pytest.fixture
def create_parking_places(db):
    park_num = database['parking_number']
    parkingplaces = ParkingPlaces.objects.bulk_create([ParkingPlaces(parking_number=num) for num in park_num])
    return parkingplaces

@pytest.fixture
def create_exist_booking():
    def _create_exist_booking(user_id):
        data = database["booking"]["exist_booking"]
        data["park_num"] = ParkingPlaces.objects.get(parking_number=data["park_num"])
        booking = Bookings.objects.create(user_id=user_id, **data)
        return booking
    return _create_exist_booking