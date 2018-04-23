import os
import requests
from typing import Dict, Any, Tuple


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
    base_url = 'https://route.cit.api.here.com/routing/7.2/'

    def __init__(self, **args):
        super().__init__(**args)

    def calculate_route(self, dlat, dlon, alat, alon) -> Tuple[float, float]:
        '''
        Return tuple with distance (km) and time (min)
        '''
        params = {
            'waypoint0': f'geo!{dlat},{dlon}',
            'waypoint1': f'geo!{alat},{alon}',
            'mode': 'shortest;car;traffic:disabled'
        }
        r = self.get(self.calculateroute, params)
        s = r['response']['route'][-1]['summary']
        return (s['distance'] / 1000, s['baseTime'] / 60)

    @property
    def calculateroute(self):
        return self.base_url + 'calculateroute.json'

    @property
    def getroute(self):
        return self.base_url + 'getroute.json'
