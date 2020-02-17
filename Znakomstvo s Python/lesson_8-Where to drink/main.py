import json
import requests
import os
from dotenv import load_dotenv
from geopy import distance

load_dotenv()


APIKEY = os.getenv('MY_API_KEY')

def fetch_coordinates(APIKEY, place):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    params = {"geocode": place, "apikey": APIKEY, "format": "json"}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    places_found = response.json()['response']['GeoObjectCollection']['featureMember']
    most_relevant = places_found[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


with open('bars.json', 'r', encoding='CP1251') as my_file:
    file_contents = json.loads(my_file.read())

    for bar_info in file_contents:
        print(bar_info['Name'], bar_info['geoData']['coordinates'][0], bar_info['geoData']['coordinates'][1])



krasnayaPL = ('55.753595', '37.621031')
Vladivostok = ('43.115536', '131.885485')
print(distance.distance(krasnayaPL, Vladivostok).km)   #Yandex возвращает долготу и широту, GeoPy принимает в обратном порядке: широту и долготу



coords = fetch_coordinates(APIKEY, input('Где вы находитесь? '))
print('Ваши координаты: ', coords) #Yandex возвращает долготу и широту




# print(first_bar_info)
# print(latitude)
# print(longitude)


