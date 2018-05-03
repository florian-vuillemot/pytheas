import random
from typing import Iterable, Tuple, List
from cities.city import get_cities
from distances.helpers import keep_in_circle,\
    DistanceCalculator, BatchCalculator, GPSPoint
from distances.haversine.haversine import haversine, time_estimation
from here_wrapper.wrapper import Routing


def get_random_path(ref_city: 'City', cities: List['City'],
                    distance: float,
                    distance_calculator: DistanceCalculator,
                    batch_calculator: BatchCalculator)\
                    -> Tuple['City', 'City']:
    '''
    Create a random path by selecting 2 cities
    This cities is at equal distance each of then and make a triangle
    '''
    _distance = distance / 3
    distances_ref = list(keep_in_circle(reference_point=ref_city,
                                        points=cities,
                                        distance_calculator=distance_calculator,
                                        batch_calculator=batch_calculator,
                                        radius=_distance))
    first_city = _get_first_city(distances_ref)
    other_cities = extract_city(first_city.name, cities)[1]
    distances_first = list(keep_in_circle(reference_point=first_city,
                                          points=other_cities,
                                          distance_calculator=distance_calculator,
                                          batch_calculator=batch_calculator,
                                          radius=_distance))
    second_city = _get_second_city(distances_ref, distances_first)
    return (first_city, second_city)


def _get_second_city(l1: List[Tuple[float, 'City']],
                     l2: List[Tuple[float, 'City']])\
                     -> 'City':
    '''
    Get cities in union between lists and return the city farest
    '''
    points = []  # type: List[Tuple[float, 'City']]
    for i in l1:
        for j in l2:
            if i[1] == j[1]:
                points.append((i[0] + j[0], i, j))
                break
    return max(points, key=lambda x: x[0])[1][1]


def _get_first_city(cities_distances: List[Tuple[float, 'City']],
                    nb_random: int = 10) -> 'City':
    '''
    Select the city with the biggest distance from nb_random city select
    '''
    rd_cities = random.sample(cities_distances, nb_random)
    return max(rd_cities, key=lambda c: c[0])[1]


def extract_city(city_name: str, cities: List['City'])\
    -> Tuple['City', List['City']]:
    '''
    Found the city in cities and return it with other cities
    '''
    other_cities = [city for city in cities if city.name != city_name]
    city = next((city for city in cities if city.name == city_name))
    return (city, other_cities)


def d_calculator(**args) -> float:
#    return Routing().calculate_route(**args)[1]
    haversine_distance = haversine(**args)
    return time_estimation(haversine_distance, 30)


def batch_calculator(**args) -> Iterable[Tuple[GPSPoint, float, float]]:
    # Base distance on time in min, not distance in km
    args['select_time'] = True
    return Routing().batch_calculate_route(**args)


if __name__ == '__main__':
    city_name = 'Bruxelles'
    distance = 240
    city, cities = extract_city(city_name, list(get_cities()))
    c1, c2 = get_random_path(ref_city=city, cities=cities,
                             distance=distance,
                             distance_calculator=None,#d_calculator,
                             batch_calculator=batch_calculator)
    print(city, c1.name, c2.name)
