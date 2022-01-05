from django.urls import reverse
import pytest
from pytest_django.asserts import assertQuerysetEqual

from bookings.models import Bookings
from conftest import database


@pytest.mark.usefixtures("create_parking_places")
class TestUserEmployee:
    @pytest.fixture(autouse=True)
    def login(self, client, create_user_employee):
        client.force_login(create_user_employee)
        yield

    def test_view_parking_places(self, client, create_parking_places):
        url = reverse('parking')
        response = client.get(url)
        assert response.status_code == 200
        assertQuerysetEqual(response.context_data['parkingplaces_list'], create_parking_places, ordered=False)

    def test_delete_parking_places(self, client):
        url = reverse('delete_parking_places', kwargs={"pk": database["parking_number"][0]})
        response = client.delete(url)
        assert response.status_code == 403

    def test_create_parking_places(self, client):
        url = reverse('create_parking_places')
        response = client.post(url)
        assert response.status_code == 403

    def test_create_normal_booking(self, client, create_user_employee, create_exist_booking):
        create_exist_booking(create_user_employee)
        data = database["booking"]["normal_booking_1"]
        url = reverse('create_booking', kwargs={"pk": data["park_num"]})
        data["user_id"] = create_user_employee.id
        assertQuerysetEqual(Bookings.objects.filter(**data), [])
        response = client.post(url, data, follow=True)
        assert response.status_code == 200
        assert Bookings.objects.get(**data, hours=int((data["end_date"] - data["start_date"]).seconds / 3600))

    def test_create_broken_booking_1(self, client, create_user_employee, create_exist_booking):
        create_exist_booking(create_user_employee)
        data = database["booking"]["broken_booking_1"]
        url = reverse('create_booking', kwargs={"pk": data["park_num"]})
        data["user_id"] = create_user_employee.id
        assertQuerysetEqual(Bookings.objects.filter(**data), [])
        client.post(url, data)
        assertQuerysetEqual(Bookings.objects.filter(**data), [])

    def test_create_broken_booking_2(self, client, create_user_employee, create_exist_booking):
        create_exist_booking(create_user_employee)
        data = database["booking"]["broken_booking_2"]
        url = reverse('create_booking', kwargs={"pk": data["park_num"]})
        data["user_id"] = create_user_employee.id
        assertQuerysetEqual(Bookings.objects.filter(**data), [])
        client.post(url, data)
        assertQuerysetEqual(Bookings.objects.filter(**data), [])

    def test_view_booking(self, client, create_user_employee, create_exist_booking):
        exist_book = create_exist_booking(create_user_employee)
        pk = database["booking"]["exist_booking"]["park_num"]
        url = reverse('bookings_list', kwargs={"pk": pk})
        response = client.get(url)
        assert response.status_code == 200
        assertQuerysetEqual(response.context_data['bookings_list'], [exist_book])

    def test_delete_booking(self, client, create_user_employee, create_exist_booking):
        exist_book = create_exist_booking(create_user_employee)
        url = reverse('delete_booking', kwargs={"pk": exist_book.id})
        response = client.delete(url)
        assert response.status_code == 403

    def test_update_booking(self, client, create_user_employee, create_exist_booking):
        exist_book = create_exist_booking(create_user_employee)
        url = reverse('update_booking', kwargs={"pk": exist_book.id})
        response = client.put(url)
        assert response.status_code == 403