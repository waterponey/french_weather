import urllib.request
import gzip
import os.path
import json
import codecs
import datetime

from city import City, CityEncoder
from api_call import APICall

api_singleton = APICall()


def download_cities(url):
    file_name = url.split('/')[-1]
    file_path = 'resources/' + file_name
    # urllib.request.urlretrieve(url, file_path)
    return gzip.open(file_path, 'r+t')


def parse2city(line):
    """
    CSV file header's is
    EU_circo;code_région;nom_région;chef-lieu_région;numéro_département;
    0        1           2          3                4
    nom_département;préfecture;numéro_circonscription;nom_commune;
    5               6          7                      8
    codes_postaux;code_insee;latitude;longitude;éloignement
    9             10         11       12        13
    """
    fields = line.split(';')
    return City(
        code_departement=fields[4],
        departement=fields[5],
        prefecture=fields[6],
        name=fields[8],
        zip_code=fields[9],
        code_insee=fields[10]
    )


def csv2cities(lines):
    return list(map(parse2city, lines))


def get_prefecture(cities):
    return list(filter(lambda x: x.is_prefecture(), cities))


def initiate_cities(url):
    file = download_cities(url)
    body = file.readlines()[1::]

    prefectures = get_prefecture(csv2cities(body))
    result = {}
    for city in prefectures:
        result[city.code_departement] = city

    return result


def url2json(url):
    response = urllib.request.urlopen(url)
    return json.loads(response.read())


def get_coordinates(city):
    print(city.name + " in")
    url = api_singleton.get_call_url("google")(city.name, city.prefecture)
    response = url2json(url)
    print(response)
    lat = response['results'][0]['geometry']['location']['lat']
    lng = response['results'][0]['geometry']['location']['lng']
    city.set_coordinates(lat, lng)


def dump_json(json_data, path):
    dump = json.dumps(json_data, cls=CityEncoder,
                      sort_keys=True, indent=2, separators=(',', ': '), ensure_ascii=False)
    f = codecs.open(path, 'w', encoding='utf8')
    f.write(dump)
    f.close()


def read_json(path):
    f = open(path)
    load = json.loads(f.read())
    f.close()
    return load


def get_weather(city, datetimes):
    result = json.loads('[]')
    timestamps = [int(dt.timestamp()) for dt in datetimes]
    for i in range(365):
        time = timestamps[i]
        date = datetimes[i]
        url = api_singleton.get_call_url()(city['latitude'], city['longitude'], time)
        response = url2json(url)
        print('At {}, for {}, with {}'.format(date, city['prefecture'], url))
        response['day'] = date.day
        response['month'] = date.month
        response['year'] = date.year
        result.append(response)
    return result


if __name__ == '__main__':

    start_date = datetime.datetime(2015, 1, 1, 12, 0, 0)
    stop_date = datetime.datetime(2015, 12, 31, 12, 0, 0)

    url_ref = ('http://www.nosdonnees.fr/wiki/images/b/b5/'
               'EUCircos_Regions_departements_circonscriptions_communes_gps.csv.gz')

    city_ref_file = 'results/cities.json'

    weather_data_dir = 'results/data'

    period = (stop_date - start_date).days
    datetimes = [start_date + datetime.timedelta(days=i) for i in range(period + 1)]

    if not os.path.isfile(city_ref_file):
        data = initiate_cities(url_ref)
        list(map(get_coordinates, data.values()))
        dump_json(data, city_ref_file)

    cities = read_json(city_ref_file)

    for key in cities.keys():
        data_path = weather_data_dir + '/' + key + '-' + cities[key]['prefecture'] + '.json'
        remaining = api_singleton.get_remaining_calls()
        if remaining < len(datetimes):
            print(remaining)
            break

        if not os.path.isfile(data_path):
            weather = get_weather(cities[key], datetimes)
            dump_json(weather, data_path)
