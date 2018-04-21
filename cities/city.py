'''
This script allow to manage city.
A city is a representation of a real city in the world.
'''
import json
import os
from typing import Union, List

# Files that contain cities of Belgium
CITIES_FILE = os.path.join(os.path.dirname(__file__), "zipcode-belgium.json")


class City():
    '''
    Represenation of a city in the physic world
    '''
    def __init__(self,
                 name: Union[None, str] = None,
                 longitude: Union[None, float] = None,
                 latitude: Union[None, float] = None) -> None:
        self.name = name

        # GPS positions
        self.lon = longitude
        self.lat = latitude

    def __str__(self):
        return f"City name: {self.name}, longitude: {self.lon}, latitude: {self.lat}"

def get_cities(filename: str = CITIES_FILE,
               city_field: str = 'city',
               longitude_field: str = 'lng',
               latitude_field: str = 'lat') -> List['City']:
    '''
    Return all cities from a json file.
    '''
    cities = []  # type: List['City']

    with open(filename) as fcities:
        for city_info in json.loads(fcities.read()):
            city = City(name=city_info[city_field],
                        longitude=city_info[longitude_field],
                        latitude=city_info[latitude_field])
            cities.append(city)

    return cities
