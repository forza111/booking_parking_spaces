from django.urls import reverse
import pytest
from pytest_django.asserts import assertQuerysetEqual

from bookings.models import Bookings,ParkingPlaces
from conftest import database

@pytest.mark.usefixtures("create_parking_places")
class TestUserManager:
    @pytest.fixture(autouse=True)
    def login(self, client, create_user_manager):
        client.force_login(create_user_manager)
        yield

    def test_view_parking_places(self, client, create_parking_places):
        url = reverse('parking')
        response = client.get(url)
        assertQuerysetEqual(response.context_data['parkingplaces_list'], create_parking_places, ordered=False)

    def test_delete_parking_places(self, client):
        pk = database["parking_number"][0]
        url = reverse('delete_parking_places', kwargs={"pk": pk})
        ParkingPlaces.objects.get(pk=pk)
        client.delete(url)
        assert ParkingPlaces.objects.filter(pk=pk).exists() == False

    def test_create_parking_places(self, client):
        url = reverse('create_parking_places')
        data = database["create_parking_number"]
        assert ParkingPlaces.objects.filter(pk=data["parking_number"]).exists() == False
        response = client.post(url,data, follow=True)
        assert response.status_code == 200
        ParkingPlaces.objects.get(pk=data["parking_number"])

    def test_create_normal_booking(self, client, create_user_manager, create_exist_booking):
        create_exist_booking(create_user_manager)
        data = database["booking"]["normal_booking_1"]
        url = reverse('create_booking', kwargs={"pk": data["park_num"]})
        data["user_id"] = create_user_manager.id
        assertQuerysetEqual(Bookings.objects.filter(**data), [])
        response = client.post(url, data, follow=True)
        assert response.status_code == 200
        assert Bookings.objects.get(**data, hours=int((data["end_date"] - data["start_date"]).seconds / 3600))

    def test_create_broken_booking_1(self, client, create_user_manager, create_exist_booking):
        create_exist_booking(create_user_manager)
        data = database["booking"]["broken_booking_1"]
        url = reverse('create_booking', kwargs={"pk": data["park_num"]})
        data["user_id"] = create_user_manager.id
        assertQuerysetEqual(Bookings.objects.filter(**data), [])
        client.post(url, data)
        assertQuerysetEqual(Bookings.objects.filter(**data), [])

    def test_create_broken_booking_2(self, client, create_user_manager, create_exist_booking):
        create_exist_booking(create_user_manager)
        data = database["booking"]["broken_booking_2"]
        url = reverse('create_booking', kwargs={"pk": data["park_num"]})
        data["user_id"] = create_user_manager.id
        assertQuerysetEqual(Bookings.objects.filter(**data), [])
        client.post(url, data)
        assertQuerysetEqual(Bookings.objects.filter(**data), [])

    def test_view_booking(self, client, create_user_manager, create_exist_booking):
        exist_book = create_exist_booking(create_user_manager)
        pk = database["booking"]["exist_booking"]["park_num"]
        url = reverse('bookings_list', kwargs={"pk": pk})
        response = client.get(url)
        assert response.status_code == 200
        assertQuerysetEqual(response.context_data['bookings_list'], [exist_book])

    def test_delete_booking(self, client, create_user_manager, create_exist_booking):
        exist_book = create_exist_booking(create_user_manager)
        url = reverse('delete_booking', kwargs={"pk": exist_book.id})
        Bookings.objects.get(pk=exist_book.id)
        response = client.delete(url, follow=True)
        assert response.status_code == 200
        assert ParkingPlaces.objects.filter(pk=exist_book.id).exists() == False

    def test_update_booking(self, client, create_user_manager, create_exist_booking):
        exist_book = create_exist_booking(create_user_manager)
        url = reverse('update_booking', kwargs={"pk": exist_book.id})
        data = database["booking"]["update_booking"]
        data.pop("park_num")
        client.post(url,data)
        assert Bookings.objects.get(pk=exist_book.id,hours=int((data["end_date"] - data["start_date"]).seconds / 3600))