'''
This script allow to manage city.
A city is a representation of a real city in the world.
'''
import json
import os
from typing import Union, Iterable

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
        self.longitude = longitude
        self.latitude = latitude

    def __str__(self):
        return f"City name: {self.name}, longitude: {self.longitude}, latitude: {self.latitude}"

    def __getitem__(self, key: str):
        return self.__dict__[key]

    def __eq__(self, oth: 'City'):
        return self.name == oth.name and\
            self.longitude == oth.longitude and\
            self.latitude == oth.latitude


def get_cities(filename: str = CITIES_FILE,
               city_field: str = 'city',
               longitude_field: str = 'lng',
               latitude_field: str = 'lat') -> Iterable['City']:
    '''
    Return all cities from a json file.
    '''
    with open(filename) as fcities:
        for city_info in json.loads(fcities.read()):
            yield City(name=city_info[city_field],
                       longitude=city_info[longitude_field],
                       latitude=city_info[latitude_field])
