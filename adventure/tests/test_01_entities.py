from datetime import date

import pytest

from adventure import models


@pytest.fixture
def car():
    return models.VehicleType(max_capacity=4)


@pytest.fixture
def van():
    return models.VehicleType(max_capacity=6)


@pytest.fixture
def tesla(car):
    return models.Vehicle(
        name="Tesla", passengers=3, vehicle_type=car, number_plate="AA-12-34"
    )


class TestVehicle:
    def test_capacity_greater_than_passengers(self, car):
        vehicle = models.Vehicle(vehicle_type=car, passengers=2)
        assert vehicle.can_start()

    def test_vehicle_overload(self, car):
        vehicle = models.Vehicle(vehicle_type=car, passengers=10)
        assert not vehicle.can_start()

    def test_vehicle_distribution(self, car, van):
        vehicle = models.Vehicle(vehicle_type=car, passengers=3)
        distribution_expected = [[True, True], [True, False]]
        assert vehicle.get_distribution() == distribution_expected

        vehicle = models.Vehicle(vehicle_type=van, passengers=5)
        distribution_expected = [[True, True], [True, True], [True, False]]
        assert vehicle.get_distribution() == distribution_expected

    @pytest.mark.parametrize(
        ["number_plate", "expected"],
        (
            ("AA-12-34", True),
            ("AA-BB-34", False),
            ("12-34-56", False),
            ("AA1234", False),
            ("AA 12 34", False),
        )
    )
    def test_valid_number_plate(self, number_plate, expected, car):
        vehicle = models.Vehicle(vehicle_type=car, passengers=3, number_plate=number_plate)
        assert vehicle.validate_number_plate() == expected


class TestJourney:
    def test_is_finished(self, tesla):
        journey = models.Journey(start=date.today(), end=date.today(), vehicle=tesla)
        assert journey.is_finished()

    def test_is_not_finished(self, tesla):
        journey = models.Journey(start=date.today(), vehicle=tesla)
        assert not journey.is_finished()
