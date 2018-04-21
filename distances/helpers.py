'''
Helpers methods for make calcul on distances.
'''
from typing import List, Dict, Tuple, Union, Any, Callable


GPSPoint = Dict[str, Union[float, Any]]
# Should take in parameters word: 'lat1', 'lat2', 'lon1', 'lon2'
DistanceCalculator = Callable[[float, float, float, float], float]


def evaluate_all_distance(distances: List[GPSPoint],
                          distance_calculator: DistanceCalculator,
                          latitude_key: str = 'latitude',
                          longitude_key: str = 'longitude')\
                          -> List[Tuple[float, GPSPoint, GPSPoint]]:
    '''
    Evaluate the distance between each element of the list
    Return a list with each distance between each elements

    Each elements of distances should contain a latitude and longitude key
    '''
    res = []  # type: List[Tuple[float, GPSPoint, GPSPoint]]

    for i in range(len(distances)):
        d1 = distances[i]
        for j in range(i + 1, len(distances)):
            d2 = distances[j]
            distance = distance_calculator(lat1=d1[latitude_key],
                                           lat2=d2[latitude_key],
                                           lon1=d1[longitude_key],
                                           lon2=d2[longitude_key])
            res.append((distance, d1, d2))

    return res
