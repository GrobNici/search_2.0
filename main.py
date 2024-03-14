import requests
import argparse
import sys
from PIL import Image
import io
import math


def lonlat_distance(a, b):
    degree = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b
    radians = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians)
    dX = abs(a_lon - b_lon) * degree * lat_lon_factor
    dY = abs(a_lat - b_lat) * degree
    distance = math.sqrt(dX * dX + dY * dY)
    return distance


def get_request(path, params):
    response = requests.get(path, params)
    if not response:
        print(f"Ошибка! Код ошибки: {response.status_code}")
        sys.exit(1)
    return response


parser = argparse.ArgumentParser()
parser.add_argument("address", type=str)
args = parser.parse_args()

path = "http://geocode-maps.yandex.ru/1.x/"
TOEKN = "40d1649f-0493-4b70-98ba-98533de7710b"
params = {
    "apikey": TOEKN,
    "geocode": args.address,
    "format": "json"}

response = get_request(path, params)
json_response = response.json()
coords = json_response = response.json(
)["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
float_coords = tuple(map(float, coords.split()))
coords = coords.replace(" ", ",")
path = "https://search-maps.yandex.ru/v1/"
TOKEN = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
drug_store_search = "аптека"
params = {
    "apikey": TOKEN,
    "text": drug_store_search,
    "lang": "ru_RU",
    "ll": coords,
    "format": "json"}
response = get_request(path, params)
json_response = response.json()
org = json_response["features"][0]
org_coords = org["geometry"]["coordinates"]
org_name = org["properties"]["CompanyMetaData"]["name"]
org_address = org["properties"]["CompanyMetaData"]["address"]
org_worktime = org["properties"]["CompanyMetaData"]["Hours"]["text"]
distance = lonlat_distance(float_coords, org_coords)

path = "http://static-maps.yandex.ru/1.x/"
params = {
    "l": "map",
    "pt": f"{coords},comma~{','.join(map(str, org_coords))},flag"
}
response = get_request(path, params)
Image.open(io.BytesIO(response.content)).show()
print("Адрес аптеки:", org_address)
print("Название аптеки:", org_name)
print("Время работы аптеки:", org_worktime)
print("Расстояние до аптеки:", round(distance, 2), "м")
print(org_coords)
