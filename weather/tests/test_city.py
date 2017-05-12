import unittest
from city import City


class TestCity(unittest.TestCase):

    def setUp(self):
        self.city = City(
            name="Perpignan",
            departement="Pyrénées-Orientales",
            code_departement="66",
            prefecture="Perpignan",
            zip_code="66000"
        )

    def test_is_prefecture_false(self):
        self.city.name = "Toulouse"
        self.assertFalse(self.city.is_prefecture())

    def test_is_prefecture_true(self):
        self.assertTrue(self.city.is_prefecture())

    def test_is_prefecture_accent(self):
        self.city.name = "Chambéry"
        self.city.prefecture = "Chambery"
        self.assertTrue(self.city.is_prefecture())

