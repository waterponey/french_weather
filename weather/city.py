# coding: utf8
# Module: city.py

import json
import unicodedata


class City:

    def __init__(self,
                 name,
                 departement,
                 code_departement,
                 prefecture,
                 zip_code,
                 code_insee='00'
                 ):
        self.name = name
        self.departement = departement
        self.code_departement = code_departement
        self.prefecture = prefecture
        self.zip_code = zip_code
        self.code_insee = code_insee

    def is_prefecture(self):
        return normalize(self.name) == normalize(self.prefecture)

    def set_coordinates(self, lat, lng):
        self.latitude = lat
        self.longitude = lng

    def to_json(self):
        data = json.loads('{}')
        data['code_departement'] = self.code_departement
        data['departement'] = self.departement
        data['prefecture'] = self.prefecture
        data['code_postal'] = self.zip_code
        data['code_insee'] = self.code_insee
        data['latitude'] = self.latitude
        data['longitude'] = self.longitude
        return data

    def dump(self):
        self.to_json()

    def __eq__(self, other):
        return self.name == other

    def __hash__(self):
        return hash(self.name)


def normalize(french_string):
    return unicodedata\
        .normalize('NFKD', french_string.lower().strip())\
        .encode('ascii', 'ignore')


class CityEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, City):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
