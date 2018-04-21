
# coding: utf-8

# In[54]:


import json
from typing import List, Tuple, Dict


# In[49]:


TIME = 30


# In[56]:


def load_json() -> List[Dict[str, str]]:
    with open("zipcode-belgium.json") as f:
        return json.loads(f.read())


# In[119]:


def filter_city() -> Dict[str, str]:
    res = {}
    for c in load_json():
        del c['zip']
        city = c['city']
        del c['city']
        res[city] = c
    return res


# In[58]:


from math import radians, cos, sin, asin, sqrt

def _haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def haversine(c1: Dict[str, str], c2: Dict[str, str]) -> float:
    return _haversine(c1['lng'], c1['lat'], c2['lng'], c2['lat'])


# In[59]:


def get_time(c1: Dict[str, str], c2: Dict[str, str]) -> float:
    d = haversine(c1, c2)
    return d * 2


# In[63]:


import copy
def get_all_distances(start: str, cities: Dict[str, str]) -> List[Tuple[str, float]]:
    _cities = copy.deepcopy(cities)
    del _cities[start]
    distances = [(name, get_time(cities[start], points)) for (name, points) in _cities.items()]
    sorted(distances, key=lambda x: x[1])
    return distances


# In[66]:


def keep_points(points: List[Tuple[str, float]], t: float) -> List[Tuple[str, float]]:
    return [point for point in points if point[1] < t]


# In[127]:


import random
def select_first_point(points: List[Tuple[str, float]]) -> Tuple[str, float]:
    _points = keep_points(points, TIME / 3)
#    return _points[0]
    ipoint = random.randint(0, len(_points) - 1)
    return _points[ipoint]


# In[128]:


def select_second_point(start: str, points: Dict[str, float],
                        first_point: Tuple[str, str], distance_start_points: Dict[str, float]):
    distances = get_all_distances(first_point[0], points)
    distances = keep_points(distances, TIME / 3)
    res = []
    for city in distances:
        for other in distance_start_points:
            if other[0] == city[0]:
                res.append((city[0], city[1], other[1]))
                break
    return min(res, key=lambda x: abs(x[1] - x[2]))
    


# In[131]:


cities = filter_city()
distances = get_all_distances('Bruxelles', cities)
first_point = select_first_point(distances)
print(first_point)
second_point = select_second_point('Bruxelles', cities, first_point, distances)
print(second_point)

