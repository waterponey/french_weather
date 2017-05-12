import unittest

from api_call import APICall


class TestAPICall(unittest.TestCase):

    def setUp(self):
        self.api_call = APICall()

    def test_get_call_url(self):
        # Given
        expected_count = self.api_call.dark_sky_keys[0]['count'] - 1
        expected_url = ('https://api.darksky.net/forecast/toto/'
                        'i,j,k?exclude=hourly,currently&units=si')

        # When
        call_function = self.api_call.get_call_url()
        count = self.api_call.dark_sky_keys[0]['count']
        result = call_function('i', 'j', 'k')

        # Then
        self.assertEqual(result, expected_url)
        self.assertEqual(count, expected_count)

    def test_get_call_url_empty(self):
        # Given
        for i in range(4):
            self.api_call.get_call_url()

        # When
        result = self.api_call.get_call_url()

        # Then
        self.assertIsNone(result)
