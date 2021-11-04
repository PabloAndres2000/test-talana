from django.db import models
from typing import List
from datetime import date
import re

class VehicleType(models.Model):
    name = models.CharField(max_length=32)
    max_capacity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=32)
    passengers = models.PositiveIntegerField()
    vehicle_type = models.ForeignKey(VehicleType, null=True, on_delete=models.SET_NULL)
    number_plate = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name

    def can_start(self) -> bool:
        return self.vehicle_type.max_capacity >= self.passengers

    def get_distribution(self) -> List[List[bool]]:
        rows = int((self.passengers + 1) / 2)
        distribution = list()
        for row in range(0, rows):
            temp_distribution = list()
            for column in range(0, 2):
                if (row == rows - 1) and (column == 1):
                    temp_distribution.append(False)
                else:
                    temp_distribution.append(True)
            distribution.append(temp_distribution)
        return distribution

    def validate_number_plate(self) -> bool:
        regex = re.compile("[A-Z]{2}-[0-9]{2}-[0-9]{2}")
        return True if regex.search(self.number_plate) else False


class Journey(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.vehicle.name} ({self.start} - {self.end})"

    def is_finished(self) -> bool:
        return self.end == date.today()
