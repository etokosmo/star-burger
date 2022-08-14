from django.contrib import admin

from .models import GeoPlace


@admin.register(GeoPlace)
class GeoPlaceAdmin(admin.ModelAdmin):
    pass
