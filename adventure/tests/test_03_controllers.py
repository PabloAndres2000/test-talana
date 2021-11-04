import pytest
import datetime
from datetime import date
from django.core import mail

from adventure import models, notifiers, repositories, usecases, views

from .test_02_usecases import MockJourneyRepository
#########
# Tests #
#########


class TestRepository:
    def test_create_vehicle(self, mocker):
        mocker.patch.object(models.Vehicle.objects, "create")
        repo = repositories.JourneyRepository()
        car = models.VehicleType()
        repo.create_vehicle(name="a", passengers=10, vehicle_type=car)
        assert models.Vehicle.objects.create.called


class TestNotifier:
    def test_send_notification(self, mocker):
        mocker.patch.object(mail, "send_mail")
        notifier = notifiers.Notifier()
        notifier.send_notifications(models.Journey())
        assert mail.send_mail.called


class TestCreateVehicleAPIView:
    def test_create(self, client, mocker):
        vehicle_type = models.VehicleType(name="car")
        mocker.patch.object(
            models.VehicleType.objects, "get", return_value=vehicle_type
        )
        mocker.patch.object(
            models.Vehicle.objects,
            "create",
            return_value=models.Vehicle(
                id=1, name="Kitt", passengers=4, vehicle_type=vehicle_type
            ),
        )
        payload = {"name": "Kitt", "passengers": 4, "vehicle_type": "car"}
        response = client.post("/api/adventure/create-vehicle/", payload)
        assert response.status_code == 201


class TestStartJourneyAPIView:
    def test_api(self, client, mocker):
        mocker.patch.object(
            views.StartJourneyAPIView,
            "get_repository",
            return_value=MockJourneyRepository(),
        )

        payload = {"name": "Kitt", "passengers": 2}
        response = client.post("/api/adventure/start/", payload)

        assert response.status_code == 201

    def test_api_fail(self, client, mocker):
        mocker.patch.object(
            views.StartJourneyAPIView,
            "get_repository",
            return_value=MockJourneyRepository(),
        )

        payload = {"name": "Kitt", "passengers": 6}
        response = client.post("/api/adventure/start/", payload)

        assert response.status_code == 400


class TestStopJourneyAPIView:

    @pytest.mark.django_db
    def test_api(self, client, mocker):
        repo = MockJourneyRepository()
        mocker.patch.object(
            views.StopJourneyAPIView,
            "get_repository",
            return_value=repo,
        )
        start_date = date.today() - datetime.timedelta(days=14)

        car = models.VehicleType.objects.create(name="car", max_capacity=4)
        vehicle = models.Vehicle.objects.create(
            name="Tesla", passengers=3, vehicle_type=car
        )
        journey = models.Journey.objects.create(vehicle=vehicle, start=start_date)


        url = f"/api/adventure/stop/{journey.pk}/"
        response = client.put(url)

        assert response.status_code == 204

    @pytest.mark.django_db
    def test_api_fail(self, client, mocker):
        repo = MockJourneyRepository()
        mocker.patch.object(
            views.StopJourneyAPIView,
            "get_repository",
            return_value=repo,
        )

        start_date = date.today() + datetime.timedelta(days=14)

        car = models.VehicleType.objects.create(name="car", max_capacity=4)
        vehicle = models.Vehicle.objects.create(
            name="Tesla", passengers=3, vehicle_type=car
        )
        journey = models.Journey.objects.create(vehicle=vehicle, start=start_date)
        
        url = f"/api/adventure/stop/{journey.pk}/"
        response = client.put(url)

        assert response.status_code == 500