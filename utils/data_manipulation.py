import osmium
import math
import pandas
import pandas as pd

# path = '/home/jakub/Pulpit/project/osm/maps/malopolskie.pbf'


class OSMHandler(osmium.SimpleHandler):
    def __init__(self, lat, lon, radius, dic):
        super(OSMHandler, self).__init__()
        self.lat = lat
        self.lon = lon
        self.radius = radius
        self.keys = list(dic.keys())
        self.dic = dic
        self.data = pd.DataFrame(columns=['name', 'lat', 'lon', 'category', 'subcategory'])

    def node(self, o):
        # o.location.lat
        # o.location.lon
        # o.visible

        # o.tags -> taglist
        # o.tags[]
        for key in self.keys:
            if key in o.tags and o.tags[key] in self.dic[key] and ('name' in o.tags or 'operator' in o.tags):
                if o.location.valid():
                    node_lat = o.location.lat
                    node_lon = o.location.lon
                    distance = self.calculate_distance(self.lat, self.lon, node_lat, node_lon)
                    if distance <= self.radius:
                        if 'name' in o.tags:
                            self.data = self.data._append({'name': o.tags['name'], 'lat': node_lat, 'lon': node_lon, 'category': key,
                                                           'subcategory': o.tags[key]}, ignore_index=True)
                        else:
                            self.data = self.data._append({'name': o.tags['operator'], 'lat': node_lat, 'lon': node_lon, 'category': key,
                                                           'subcategory': o.tags[key]}, ignore_index=True)


    def acc(self):
        return self.data

    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        # Metoda Haversina do obliczania odległości
        # Konwersja stopni na radiany
        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        # Różnice szerokości i długości geograficznych
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        # Wzór haversine
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        radius_of_earth = 6371  # Promień Ziemi w kilometrach
        distance = radius_of_earth * c

        return distance



























# dic = {'amenity': ['bar', 'biergarten', 'cafe', 'fast_food', 'food_court', 'ice_cream', 'pub', 'restarurant', 'school', 'library', 'atm', 'bank', 'hospital', 'veterinary', 'pharmacy', 'church'],
#        'building': ['church']}
#
#
#
# # dic = {'amenity': {'food': ['bar', 'biergarten', 'cafe', 'fast_food', 'food_court', 'ice_cream', 'pub', 'restaurant'],
# #                    'education': ['school', 'library'],
# #                    'financial': ['atm', 'bank'],
# #                    'healthcare': ['hospital', 'veterinary', 'pharmacy']
# #                    },
# #        'building': {'religious': ['church']}
# #        }
#
# # Wpisz koordynaty i promień obszaru
# latitude = 50.0791599
# longitude = 19.9071159
# radius = 1  # w kilometrach
#
# # Użycie klasy HotelHandler z określonym obszarem
# h = OSMHandler(latitude, longitude, radius, dic)
# h.apply_file(path)
#
# print(h.acc())










# from geopy.geocoders import Nominatim
#
# # Inicjalizacja geokodera Nominatim
# geolocator = Nominatim(user_agent="my_geocoder")
#
# # Adres do wyszukania
# address = ("wiejska 10 warszawa")
#
# # Wyszukiwanie adresu
# location = geolocator.geocode(address)
#
# # Wyświetlenie współrzędnych
# if location:
#     print("Współrzędne dla adresu '{}':".format(address))
#     print("Szerokość geograficzna:", location.latitude)
#     print("Długość geograficzna:", location.longitude)
# else:
#     print("Nie można znaleźć współrzędnych dla adresu '{}'. Spróbuj podać inny adres.".format(address))
