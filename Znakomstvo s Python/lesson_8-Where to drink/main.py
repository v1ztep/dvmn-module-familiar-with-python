import json
import requests
import os
from dotenv import load_dotenv
from geopy import distance
import folium
from flask import Flask


def fetch_coordinates(apikey, place):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    params = {"geocode": place, "apikey": apikey, "format": "json"}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    places_found = response.json()['response']['GeoObjectCollection']['featureMember']
    most_relevant = places_found[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def get_bar_distance(bar_around):
    return bar_around['distance']


def bars_around_user():
    with open('index.html', encoding='utf-8') as file:
        return file.read()


def main():
    load_dotenv()
    apikey = os.getenv('YANDEX_GEOCODER_APIKEY')
    nearest_bars_amount = 5

    user_lon, user_lat = fetch_coordinates(apikey, input('Введите своё местоположение: '))

    bars_with_distance = []

    with open('bars.json', 'r', encoding='CP1251') as my_file:
        bars_contents = json.loads(my_file.read())

        for bar_info in bars_contents:
            bar_latitude = bar_info['geoData']['coordinates'][1]
            bar_longitude = bar_info['geoData']['coordinates'][0]
            bar_name = bar_info['Name']

            bar_info_with_distance = {
                'distance': distance.distance((user_lat, user_lon), (bar_latitude, bar_longitude)).km,
                'latitude': bar_latitude,
                'longitude': bar_longitude,
                'title': bar_name
            }
            bars_with_distance.append(bar_info_with_distance)

    nearest_bars = sorted(bars_with_distance, key=get_bar_distance)[:nearest_bars_amount]

    user_and_bars_on_map = folium.Map(
        location=[user_lat, user_lon],
        zoom_start=15
    )

    folium.Marker(
        location=[user_lat, user_lon],
        popup='User',
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(user_and_bars_on_map)

    for bar in nearest_bars:
        folium.Marker(
            location=[bar['latitude'], bar['longitude']],
            popup=bar['title'],
            icon=folium.Icon(color='green')
        ).add_to(user_and_bars_on_map)

    user_and_bars_on_map.save('index.html')

    app = Flask(__name__)
    app.add_url_rule('/', 'bars around', bars_around_user)
    app.run('127.0.0.1')


if __name__ == '__main__':
    main()
