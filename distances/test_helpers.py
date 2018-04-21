import unittest
from helpers import evaluate_all_distance


class TestHelpers(unittest.TestCase):
    distances = [
        {'id': 0, 'lat': 1, 'lon': 1},
        {'id': 1, 'lat': 2, 'lon': 2},
        {'id': 2, 'lat': 3, 'lon': 3},
        {'id': 3, 'lat': 4, 'lon': 4},
        {'id': 4, 'lat': 5, 'lon': 5}
    ]

    def test_evaluate_all_distance(self):
        results_distances = evaluate_all_distance(
            distances=self.distances,
            distance_calculator=distance_calculator,
            latitude_key='lat',
            longitude_key='lon'
        )

        id_d1, id_d2, nb_distances = 0, 1, len(self.distances)
        for distance in results_distances:
            r, d1, d2 = distance

            self.assertEqual(r, 42.42)
            self.assertEqual(d1['id'], id_d1)
            self.assertEqual(d2['id'], id_d2)
            id_d2 += 1
            if id_d2 == nb_distances:
                id_d1 += 1
                id_d2 = id_d1 + 1


def distance_calculator(lat1: float, lon1: float,
                        lat2: float, lon2: float) -> float:
    return 42.42


if __name__ == '__main__':
    unittest.main()
