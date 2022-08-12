from django.db import models
from django.utils import timezone


class GeoPlace(models.Model):
    address = models.CharField(
        verbose_name="Адрес",
        max_length=100,
        unique=True
    )
    latitude = models.FloatField(
        verbose_name='Широта',
        blank=True,
        null=True)
    longitude = models.FloatField(
        verbose_name="Долгота",
        blank=True,
        null=True)
    updated_at = models.DateTimeField(
        'Время запроса к геокодеру',
        default=timezone.now,
        db_index=True
    )

    def __str__(self):
        return f"{self.address} - {self.updated_at}"
