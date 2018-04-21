import unittest
from city import City, get_cities

class TestCity(unittest.TestCase):
    init_values = [
        {},
        {'name': 'Paris'},
        {'latitude': 42.42},
        {'longitude': 42.42},
        {'name': 'Paris', 'latitude': 42.42, 'longitude': 42.42},
        {'name': 'London', 'latitude': 42.42, 'longitude': 84.84}
    ]

    def test_init(self):
        for values in self.init_values:
            city = City(**values)
            self.assertEqual(city.name, values.get('name', None))
            self.assertEqual(city.latitude, values.get('latitude', None))
            self.assertEqual(city.longitude, values.get('longitude', None))


class TestGetCities(unittest.TestCase):
    def test_numbers(self):
        self.assertEqual(len(list(get_cities())), 2757)


if __name__ == '__main__':
    unittest.main()
