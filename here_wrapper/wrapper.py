import os
import requests
from typing import Dict, Any, Tuple, Iterable, Union, List
GPSPoint = Dict[str, Union[float, Any]]


class HereError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Here():
    '''
    Wrapper around the Here API
    '''
    def __init__(self) -> None:
        pass

    def get(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        params['app_id'] = os.environ['HERE_APP_ID']
        params['app_code'] = os.environ['HERE_APP_CODE']
        r = requests.get(url, params=params)
        if r.status_code == 200:
            return r.json()
        raise HereError(f'Receive status code {r.status_code}')


class Routing(Here):
    '''
    Routing wrapper for Here
    '''

    def __init__(self, **args):
        super().__init__(**args)

    def calculate_route(self, lat1, lon1, lat2, lon2) -> Tuple[float, float]:
        '''
        Return tuple with distance (km) and time (min)
        '''
        params = {
            'waypoint0': f'geo!{lat1},{lon1}',
            'waypoint1': f'geo!{lat2},{lon2}',
            'mode': 'shortest;car;traffic:disabled'
        }
        r = self.get(self.calculateroute, params)
        s = r['response']['route'][-1]['summary']
        return (s['distance'] / 1000, s['baseTime'] / 60)

    def batch_calculate_route(self, reference: GPSPoint,
                              points: List[GPSPoint],
                              **args)\
                              -> Iterable[Tuple[GPSPoint, float, float]]:
        '''
        Return point, distance and time estimation between points and reference
        '''
        for i in range(0, len(points), 100):
            for r in self._batch_calculate_route(reference,
                                                 points[i:i + 100],
                                                 **args):
                yield r

    def _batch_calculate_route(self, reference: GPSPoint,
                               points: List[GPSPoint],
                               latitude_key: str, longitude_key: str,
                               select_time: bool = False)\
                               -> Iterable[Tuple[GPSPoint, float, float]]:
        params = {
            'start0': f'geo!{reference[latitude_key]},{reference[longitude_key]}',
            'mode': 'shortest;car;traffic:disabled',
            'summaryAttributes': 'distance,traveltime'
        }
        for idx, p in enumerate(points):
            pos = f'geo!{p[latitude_key]},{p[longitude_key]}'
            params[f'destination{idx}'] = pos
        r = self.get(self.matrixroute, params)
        distances = r['response']['matrixEntry']
        for d in distances:
            mesure = d['summary']['travelTime'] / 60 if select_time\
                     else d['summary']['distance'] / 1000
            yield points[d['destinationIndex']], mesure

    @property
    def calculateroute(self):
        return 'https://route.cit.api.here.com/routing/7.2/calculateroute.json'

    @property
    def getroute(self):
        return 'https://matrix.route.cit.api.here.com/routing/7.2/getroute.json'

    @property
    def matrixroute(self):
        return 'https://matrix.route.cit.api.here.com/routing/7.2/calculatematrix.json'
