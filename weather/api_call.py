import json
import unicodedata


class APICall:

    def __init__(self):
        f = open('resources/private_keys.json', 'r')
        self.dark_sky_keys = json.loads(f.read())
        f.close()

    def get_call_url(self, target='darksky'):
        if target == 'darksky':
            for data in self.dark_sky_keys:
                count = data['count']
                key = data['key']
                if count > 0:
                    data['count'] = count - 1
                    return (lambda lat, lng, time:
                                   dark_sky_call(key, lat, lng, time))
        else:
            return google_geocode_call

    def get_remaining_calls(self):
        count = 0
        for data in self.dark_sky_keys:
            count = count + data['count']
        return count


def dark_sky_call(key, latitude, longitude, time):
    return ('https://api.darksky.net/forecast/' + key +
            '/{},{},{}?exclude=hourly,currently&units=si'.format(latitude, longitude, time))


def google_geocode_call(city, departement):
    return ('https://maps.googleapis.com/maps/api/geocode/json?address=' +
            str(unicodedata
                .normalize('NFKD', (city + ", " + departement).replace(" ", "+"))
                .encode('ascii', 'ignore')))
