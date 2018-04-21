import unittest
from helpers import evaluate_all_distance, keep_in_circle


class TestHelpers(unittest.TestCase):
    points = [
        {'id': 0, 'lat': 1, 'lon': 1},
        {'id': 1, 'lat': 2, 'lon': 2},
        {'id': 2, 'lat': 3, 'lon': 3},
        {'id': 3, 'lat': 4, 'lon': 4},
        {'id': 4, 'lat': 5, 'lon': 5}
    ]

    def test_evaluate_all_distance(self):
        results_distances = evaluate_all_distance(
            points=self.points,
            distance_calculator=distance_calculator,
            latitude_key='lat',
            longitude_key='lon'
        )

        id_d1, id_d2, nb_distances = 0, 1, len(self.points)
        for distance in results_distances:
            r, d1, d2 = distance

            self.assertEqual(r, 42.42)
            self.assertEqual(d1['id'], id_d1)
            self.assertEqual(d2['id'], id_d2)
            id_d2 += 1
            if id_d2 == nb_distances:
                id_d1 += 1
                id_d2 = id_d1 + 1

    def test_keep_in_circle(self):
        nb_points = len(self.points) - 1
        params = {
            'reference_point': self.points[0],
            'points': self.points[1:],
            'latitude_key': 'lat',
            'longitude_key': 'lon'
        }
        # Radius <= 2
        params['distance_calculator'] = radius_distance_eq2_or_eq1
        self.assertEqual(len(list(keep_in_circle(radius=2, **params))), 2)
        # Radius == 3
        params['distance_calculator'] = radius_distance_eq3
        self.assertEqual(len(list(keep_in_circle(radius=1, **params))), 1)
        # All radius
        params['distance_calculator'] = radius_distance_all_1
        self.assertEqual(len(list(keep_in_circle(radius=2, **params))), nb_points)
        # No radius
        params['distance_calculator'] = radius_distance_all_1
        self.assertEqual(len(list(keep_in_circle(radius=0, **params))), 0)


def distance_calculator(lat1: float, lon1: float,
                        lat2: float, lon2: float) -> float:
    return 42.42


def radius_distance_eq2_or_eq1(lat1: float, lon1: float,
                               lat2: float, lon2: float) -> float:
    return 1 if lat2 == 2 or lat2 == 3 else 50

def radius_distance_eq3(lat1: float, lon1: float,
                        lat2: float, lon2: float) -> float:
    return 1 if lat2 == 3 else 50

def radius_distance_all_1(lat1: float, lon1: float,
                          lat2: float, lon2: float) -> float:
    return 1


if __name__ == '__main__':
    unittest.main()
