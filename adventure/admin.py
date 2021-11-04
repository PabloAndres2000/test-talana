from django.contrib import admin

from adventure import models

admin.site.register(models.VehicleType)
admin.site.register(models.Vehicle)
admin.site.register(models.Journey)
