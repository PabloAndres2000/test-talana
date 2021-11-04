import pytest
import datetime
from datetime import date
from django.utils import timezone
from adventure import models, notifiers, repositories, usecases

#########
# Mocks #
#########


class MockJourneyRepository(repositories.JourneyRepository):
    def get_or_create_car(self) -> models.VehicleType:
        return models.VehicleType(name="car", max_capacity=4)

    def create_vehicle(
        self, name: str, passengers: int, vehicle_type: models.VehicleType
    ) -> models.Vehicle:
        return models.Vehicle(
            name=name, passengers=passengers, vehicle_type=vehicle_type
        )

    def create_journey(self, vehicle) -> models.Journey:
        return models.Journey(vehicle=vehicle, start=timezone.now().date())


class MockNotifier(notifiers.Notifier):
    def send_notifications(self, journey: models.Journey) -> None:
        pass


#########
# Tests #
#########

class TestStartJourney:
    def test_start(self):
        repo = MockJourneyRepository()
        notifier = MockNotifier()
        data = {"name": "Kitt", "passengers": 2}
        usecase = usecases.StartJourney(repo, notifier).set_params(data)
        journey = usecase.execute()

        assert journey.vehicle.name == "Kitt"

    def test_cant_start(self):
        repo = MockJourneyRepository()
        notifier = MockNotifier()
        data = {"name": "Kitt", "passengers": 6}
        usecase = usecases.StartJourney(repo, notifier).set_params(data)
        with pytest.raises(usecases.StartJourney.CantStart):
            journey = usecase.execute()


class TestStopJourney:
    def test_can_stop(self):
        repo = MockJourneyRepository()
        car = repo.get_or_create_car()
        vehicle = repo.create_vehicle(
            name="Tesla", passengers=3, vehicle_type=car
        )

        data = {"end_date": f"{date.today()}"}
        start_date = datetime.date.today() - datetime.timedelta(days=14)
        journey = models.Journey(vehicle=vehicle, start=start_date)

        usecase = usecases.StopJourney(repo, journey).set_params(data)
        usecase.execute()

        assert journey.end == date.today()

    def test_cant_stop(self):
        repo = MockJourneyRepository()

        car = repo.get_or_create_car()
        vehicle = repo.create_vehicle(
            name="Tesla", passengers=3, vehicle_type=car
        )

        data = {"end_date": f"{date.today()}"}
        start_date = date.today() + datetime.timedelta(days=14)

        journey = models.Journey(vehicle=vehicle, start=start_date)
        usecase = usecases.StopJourney(repo, journey).set_params(data)

        with pytest.raises(usecases.StopJourney.CantStop):
            usecase.execute()