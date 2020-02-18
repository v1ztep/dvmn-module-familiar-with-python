import json
import requests
import os
from dotenv import load_dotenv
from geopy import distance
import folium


def fetch_coordinates(APIKEY, place):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    params = {"geocode": place, "apikey": APIKEY, "format": "json"}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    places_found = response.json()['response']['GeoObjectCollection']['featureMember']
    most_relevant = places_found[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def get_bar_distance(bar_around):
    return bar_around['distance']

def main():
    load_dotenv()
    APIKEY = os.getenv('YANDEX_GEOCODER_APIKEY')
    NEAREST_BARS_AMOUNT = 5

    user_lon, user_lat = fetch_coordinates(APIKEY, input('Введите своё местоположение: '))

    bars_with_distance = []

    with open('bars.json', 'r', encoding='CP1251') as my_file:
        bars_contents = json.loads(my_file.read())

        for bar_info in bars_contents:
            bar_info_with_distance = {
                'distance': distance.distance((user_lat, user_lon), (bar_info['geoData']['coordinates'][1], bar_info['geoData']['coordinates'][0])).km,
                'latitude': bar_info['geoData']['coordinates'][1],
                'longitude': bar_info['geoData']['coordinates'][0],
                'title': bar_info['Name']
            }
            bars_with_distance.append(bar_info_with_distance)

    sorted_bars = sorted(bars_with_distance, key=get_bar_distance)[:NEAREST_BARS_AMOUNT]

    user_and_bars_on_map = folium.Map(
        location=[user_lat, user_lon],
        zoom_start=15
    )

    folium.Marker(
        location=[user_lat, user_lon],
        popup='User',
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(user_and_bars_on_map)

    for bar in sorted_bars:
        folium.Marker(
            location=[bar['latitude'], bar['longitude']],
            popup=bar['title'],
            icon=folium.Icon(color='green')
        ).add_to(user_and_bars_on_map)

    user_and_bars_on_map.save('index.html')



if __name__ == '__main__':
    main()
