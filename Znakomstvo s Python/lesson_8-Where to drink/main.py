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


def get_bar_distance(bars_around):
    return bars_around['distance']

def main():
    load_dotenv()
    APIKEY = os.getenv('YANDEX_GEOCODER_APIKEY')

    my_coordinates = fetch_coordinates(APIKEY, input('Где вы находитесь? '))

    bars_around = []

    with open('bars.json', 'r', encoding='CP1251') as my_file:
        file_contents = json.loads(my_file.read())

        for bar_info in file_contents:
            bar_around_info = {
                'distance': distance.distance((my_coordinates[1], my_coordinates[0]), (bar_info['geoData']['coordinates'][1], bar_info['geoData']['coordinates'][0])).km,
                'latitude': bar_info['geoData']['coordinates'][1],
                'longitude': bar_info['geoData']['coordinates'][0],
                'title': bar_info['Name']
            }
            bars_around.append(bar_around_info)

    sorted_five_bars = sorted(bars_around, key=get_bar_distance)[:5]

    me_and_five_bars_on_map = folium.Map(
        location=[my_coordinates[1], my_coordinates[0]],
        zoom_start=15
    )

    folium.Marker(
        location=[my_coordinates[1], my_coordinates[0]],
        popup='Me',
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(me_and_five_bars_on_map)

    for bar in sorted_five_bars:
        folium.Marker(
            location=[bar['latitude'], bar['longitude']],
            popup=bar['title'],
            icon=folium.Icon(color='green')
        ).add_to(me_and_five_bars_on_map)

    me_and_five_bars_on_map.save('index.html')



if __name__ == '__main__':
    main()
