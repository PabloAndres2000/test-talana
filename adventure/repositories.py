from django.utils import timezone
from datetime import date
from adventure import models

class JourneyRepository:
    def get_or_create_car(self) -> models.VehicleType:
        car, _ = models.VehicleType.objects.get_or_create(name="car", max_capacity=5)
        return car

    def create_vehicle(
        self, name: str, passengers: int, vehicle_type: models.VehicleType
    ) -> models.Vehicle:
        return models.Vehicle.objects.create(
            name=name, passengers=passengers, vehicle_type=vehicle_type
        )

    def create_journey(self, vehicle: models.Vehicle) -> models.Journey:
        return models.Journey.objects.create(
            vehicle=vehicle, start=timezone.now().date()
        )

    def get_journey_by_pk(self, pk: int) -> models.Journey:
        return models.Journey.objects.get(
            pk=pk
        )

    def stop_journey(self, journey: models.Journey, end_date: date) -> models.Journey:
        journey.end = end_date
        return journey
