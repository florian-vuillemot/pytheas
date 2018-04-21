'''
Haversine basic implementation.
Calcul distance between 2 GPS points.
'''
from math import radians, cos, sin, asin, sqrt

# Radius of earth in kilometers. Use 3956 for miles
EARTH_RADIUS = 6371


def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    Result: Km
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon, dlat = lon2 - lon1, lat2 - lat1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    return c * EARTH_RADIUS


def time_estimation(km_distance: float, km_time_average: float) -> float:
    '''
    Return the time estimation for make the distance
    km_time_average: average time for make one km
    '''
    # TODO: Use Fuzzy logic
    return km_distance / km_time_average
