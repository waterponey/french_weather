import unittest

from main import *

class TestMain(unittest.TestCase):

    def setUp(self):
        self.city1 = City(
            name="Perpignan",
            departement="Pyrénées-Orientales",
            code_departement="66",
            prefecture="Perpignan",
            zip_code="66000"
        )

        self.city2 = City(
            name="Céret",
            departement="Pyrénées-Orientales",
            code_departement="66",
            prefecture="Perpignan",
            zip_code="66000"
        )

    def test_get_prefecture(self):
        # Given
        cities = [self.city1, self.city2]
        expected = [self.city1]

        # When
        result = get_prefecture(cities)

        # Then
        self.assertEqual(result, expected)
