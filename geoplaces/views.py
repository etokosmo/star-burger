import requests
from django.shortcuts import render

from star_burger import settings
from .models import GeoPlace


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection'][
        'featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def get_addresses_coordinates(addresses: list) -> dict:
    addresses_coordinates = {}
    geo_places = GeoPlace.objects.filter(address__in=addresses)
    geo_places_addresses = [geo_place.address for geo_place in geo_places]
    for address in addresses:
        if address in geo_places_addresses:
            continue
        try:
            lon, lat = fetch_coordinates(settings.YANDEX_GEO_API_TOKEN,
                                         address)
        except TypeError:
            continue
        addresses_coordinates[address] = (lat, lon)
        place = GeoPlace(address=address, latitude=lat, longitude=lon)
        place.save()
    for place in geo_places:
        if place.address not in addresses_coordinates:
            addresses_coordinates[place.address] = (
                place.latitude, place.longitude)
    return addresses_coordinates
