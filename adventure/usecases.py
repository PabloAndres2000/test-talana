from __future__ import annotations
from datetime import date
from .notifiers import Notifier
from .repositories import JourneyRepository
from adventure import models


class StartJourney:
    def __init__(self, repository: JourneyRepository, notifier: Notifier):
        self.repository = repository
        self.notifier = notifier

    def set_params(self, data: dict) -> StartJourney:
        self.data = data
        return self

    def execute(self) -> None:
        car = self.repository.get_or_create_car()
        vehicle = self.repository.create_vehicle(vehicle_type=car, **self.data)
        if not vehicle.can_start():
            raise StartJourney.CantStart("vehicle can't start")

        journey = self.repository.create_journey(vehicle)
        self.notifier.send_notifications(journey)
        return journey

    class CantStart(Exception):
        pass

class StopJourney:
    def __init__(self, repository: JourneyRepository, journey: models.Journey):
        self.repository = repository
        self.journey = journey

    def set_params(self, data: dict) -> StopJourney:
        self.data = data
        return self

    def execute(self) -> None:
        is_started = self.journey.start < date.today()

        if is_started:
            self.repository.stop_journey(journey=self.journey, end_date=date.today())
        else:
            raise StopJourney.CantStop("Journey can't stop because is not started")

    class CantStop(Exception):
        pass