import osmium
import math

path = '/home/jakub/Pulpit/project/osm/maps/malopolskie.pbf'


class OSMHandler(osmium.SimpleHandler):
    def __init__(self, lat, lon, radius):
        super(OSMHandler, self).__init__()
        self.lat = lat
        self.lon = lon
        self.radius = radius
        self.hotels = []
        self.tags = []

    def node(self, o):
        # o.location.lat
        # o.location.lon
        # o.visible

        # o.tags -> taglist
        # o.tags[]
        if 'tourism' in o.tags and o.tags['tourism'] == 'hotel' and 'name' in o.tags:
            print(type(o))
            print(type(o.tags))
            if o.location.valid():  # Sprawdź, czy lokalizacja jest ważna
                node_lat = o.location.lat
                node_lon = o.location.lon
                distance = self.calculate_distance(self.lat, self.lon, node_lat, node_lon)
                if distance <= self.radius:
                    self.hotels.append(o.tags['name'])
    def acc(self):
        return self.tags

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




dic = {'amenity': {'food': ['bar', 'biergarten', 'cafe', 'fast_food', 'food_court', 'ice_cream', 'pub', 'restaurant'],
                   'education': ['school', 'library'],
                   'financial': ['atm', 'bank'],
                   'healthcare': ['hospital', 'veterinary','pharmacy']
                   },
       'building': {'religious': ['church']}
}

# Wpisz koordynaty i promień obszaru
latitude = 50.0614
longitude = 19.9372
radius = 1  # w kilometrach

# Użycie klasy HotelHandler z określonym obszarem
h = OSMHandler(latitude, longitude, radius)
h.apply_file(path)

# Wyświetlenie hoteli w określonym obszarze
print("Hotele w określonym obszarze:")
for hotel in h.hotels:
    print(hotel)
print(len(h.hotels))






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
