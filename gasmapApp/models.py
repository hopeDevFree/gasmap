from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=200)
    lat = models.FloatField(default=0.0)
    lon = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class FuelType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ServiceType(models.Model):
    type = models.CharField(max_length=200)

    def __str__(self):
        return self.type


class StationFuelService(models.Model):
    station = models.ForeignKey('Station', on_delete=models.CASCADE)
    fuel = models.ForeignKey(FuelType, on_delete=models.CASCADE)
    service = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    price = models.IntegerField()

    def __str__(self):
        return self.station.name + ", " + self.fuel.name + ", " + self.service.name


class Station(models.Model):
    id = models.BigIntegerField(primary_key=True)
    image = models.ImageField()
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    details_url = models.URLField()
    last_update = models.DateTimeField(verbose_name="datetime update")
    fuel_types = models.ManyToManyField(FuelType, through=StationFuelService)
    service_types = models.ManyToManyField(ServiceType, through=StationFuelService)

    def __str__(self):
        return self.name
