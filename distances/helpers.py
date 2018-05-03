'''
Helpers methods for make calcul on distances.
We considere that a distance can be in km or hours.
'''
from typing import List, Dict, Tuple, Union, Any, Callable, Iterable


GPSPoint = Dict[str, Union[float, Any]]
# Should take in parameters word: 'lat1', 'lat2', 'lon1', 'lon2'
DistanceCalculator = Callable[[float, float, float, float], float]
# Should take in parameters: reference, points, latitude_key, longitude_key
BatchCalculator = Callable[
    [GPSPoint, List[GPSPoint], str, str], Iterable[Tuple[float, GPSPoint]]
]


def evaluate_all_distance(points: List[GPSPoint],
                          **args)\
                          -> Iterable[Tuple[float, GPSPoint, GPSPoint]]:
    '''
    Evaluate the distance between each element of the list
    Return a list with each distance between each elements

    Each elements of points should contain a latitude and longitude key
    '''
    for i in range(len(points)):
        pnt = points[i]
        for (d, oth) in distances_from_point(pnt, points[i + 1:], **args):
            yield (d, pnt, oth)


def keep_in_circle(reference_point: GPSPoint,
                   points: List[GPSPoint],
                   radius: float,
                   **args)\
                   -> Iterable[Tuple[float, GPSPoint]]:
    '''
    Keep all element points in a circle around the reference point
    '''
    for (d, oth) in distances_from_point(reference_point, points, **args):
        if d <= radius:
            yield (d, oth)


def distances_from_point(reference: GPSPoint,
                         points: List[GPSPoint],
                         distance_calculator: DistanceCalculator = None,
                         batch_calculator: BatchCalculator = None,
                         latitude_key: str = 'latitude',
                         longitude_key: str = 'longitude')\
                         -> Iterable[Tuple[float, GPSPoint]]:
    '''
    Return distance of each point from reference
    '''
    # This method is not test directly
    # Test though other method
    assert(distance_calculator or batch_calculator)

    if batch_calculator:
        batch = batch_calculator(reference=reference,
                                 points=points,
                                 latitude_key=latitude_key,
                                 longitude_key=longitude_key)
        for (pnt, mesure) in batch:
            yield mesure, pnt

    else:
        for point in points:
            distance = distance_calculator(lat1=reference[latitude_key],
                                           lon1=reference[longitude_key],
                                           lat2=point[latitude_key],
                                           lon2=point[longitude_key])
            yield distance, point
