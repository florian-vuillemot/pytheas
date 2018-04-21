import unittest
from haversine import haversine, time_estimation


class TestHaversine(unittest.TestCase):
    '''
    No need float precision.
    -> Equality is done in integer value.
    '''
    data_haversine = [
        (347.3, {'lon1': -99.436554, 'lat1': 41.507483,
                 'lon2': -98.315949, 'lat2': 38.504048}),
        (343.657, {'lon1': 2.352222, 'lat1': 48.856614,
                   'lon2': -0.127758, 'lat2': 51.507351}),
        (15.453, {'lon1': 4.399100, 'lat1': 50.714690,
                   'lon2': 4.351721, 'lat2': 50.850346}),
    ]
    data_time_estimation = [
        (3, {'km_distance': 90, 'km_time_average': 30}),
        (1, {'km_distance': 90, 'km_time_average': 90}),
        (3, {'km_distance': 500, 'km_time_average': 130})
    ]

    def test_haversine(self):
        for d in self.data_haversine:
            # Km precision is suffisant, no need meters
            self.assertEqual(int(d[0]), int(haversine(**d[1])))

    def test_time_estimation(self):
        for d in self.data_time_estimation:
            self.assertEqual(int(d[0]), int(time_estimation(**d[1])))


if __name__ == '__main__':
    unittest.main()
