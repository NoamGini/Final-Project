from backend.src.mongoDB import *
import base64
import requests
from urllib.parse import urlparse, parse_qs
import re
import pyjsparser
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool
import pandas as pd
from datetime import datetime, timedelta, timezone
import logging
#from google.cloud import storage
from pyarrow.feather import write_feather
import pyarrow as pa
from math import sin, cos, sqrt, atan2, radians
import googlemaps
import numpy as np
from geopy.distance import geodesic
import asyncio
import functools
import aiohttp
from bs4 import BeautifulSoup


PARKING_LIST_URL = 'https://centralpark.co.il/רשימת-חניונים/'
STATUS_TO_FLOAT = {'פנוי': 0, '': 1}
ISRAEL_TZ = timezone(timedelta(hours=2))
# Google Maps API key
# api_key = "AIzaSyA4DV1zbLCECX_kcZAWA4vCoti9Hm156W4"
#api_key ="AIzaSyDKupYcq3t0hyHTn-YQRriH57ch-Ekw0cs"
api_key='AIzaSyDGG3PgHwpThGyw-BeKsaTs3mS5eS3BZXE'


def get_gps_coordinates(hebrew_address):
    # Set the API endpoint and your API key
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"

    # Set the address and other parameters
    params = {
        "address": hebrew_address,
        "key": api_key,
        "language": "he"
    }

    # Make the API request
    response = requests.get(endpoint, params=params)
    # Get the latitude and longitude from the response
    latitude = response.json()["results"][0]["geometry"]["location"]["lat"]
    longitude = response.json()["results"][0]["geometry"]["location"]["lng"]

    # Print the latitude and longitude
    print(latitude)
    print(longitude)

    return latitude, longitude


# def find_closest_places(places, latitude, longitude):
#     THRESHOLD_DISTANCE = 2  # threshold distance in kilometers
#
#     # Initialize a list to store the closest places
#     closest_places = []
#
#     # Define the client object
#     gmaps = googlemaps.Client(api_key)
#
#     # Define the origin point by latitude and longitude
#     origin = (latitude, longitude)
#
#     # Loop through the list of places and calculate the distance from each place to the origin point
#     for place in places:
#         # Define the destination point by latitude and longitude
#         destination = (float(place['latitude']), float(place['longitude']))
#
#         # Calculate the distance between the origin and destination points
#         distance_km = geodesic(origin, destination).km
#
#         # Check if the distance is within the threshold distance
#         if distance_km <= THRESHOLD_DISTANCE:
#             # Define the transportation mode (walking)
#             mode = "walking"
#
#             # Define the departure time
#             departure_time = datetime.now()
#
#             # Call the directions API
#             result = gmaps.directions(origin, destination, mode=mode, departure_time=departure_time)
#
#             # Extract the distance in meters
#             distance_meters = result[0]['legs'][0]['distance']['value']
#
#             # Extract the duration
#             duration = result[0]['legs'][0]['duration']['text']
#
#             closest_places.append((place, distance_meters, duration))
#
#             # If we have found 10 places, break out of the loop
#             if len(closest_places) == 10:
#                 break
#
#     # Sort the list of tuples by distance in ascending order
#     closest_places.sort(key=lambda x: x[1])
#
#     # Return the list of closest places
#     return closest_places


def find_closest_places(places, latitude, longitude):
    # Initialize a list to store the closest parking lots from each parking lot to the GPS coordinate
    closest_places = []

    # Loop through the list of places and calculate the distance from each place to the GPS coordinate
    for place in places:
        # Define the client object
        gmaps = googlemaps.Client(api_key)

        # Define the two points by latitude and longitude
        point1 = (latitude, longitude)  # example point
        point2 = (float(place['GPSLattitude']), float(place['GPSLongitude']))  # example point

        # Define the transportation mode (walking)
        mode = "walking"

        # Define the departure time
        departure_time = datetime.now()

        # Call the directions API
        result = gmaps.directions(point1, point2, mode=mode, departure_time=departure_time)

        # Extract the distance in meters
        distance_meters = result[0]['legs'][0]['distance']['value']

        # Extract the duration
        duration = result[0]['legs'][0]['duration']['text']
        # int_duration = int(duration.split()[0])

        closest_places.append((place, distance_meters, duration))
        # If we have found 10 places, break out of the loop
        if len(closest_places) == 10:
            break

    # Find the index of the minimum distance in the list
    # min_index = distances.index(min(distances))
    # sort the list of tuples by distance in ascending order

    closest_places.sort(key=lambda x: x[1])
    # print(closest_places)
    # Return the name of the place with the minimum distance
    return closest_places


def get_parking_lot_info(parking_name):
    element_status = ''
    parking_lot_info = {}
    PARKING_LOT_URL = f'https://centralpark.co.il/parking/{parking_name}/'
    soup = BeautifulSoup(requests.get(PARKING_LOT_URL).content, features="html.parser")
    status = soup.find("div", class_="wrap_parking_detailes")
    script = status.findChild("script").text.strip()
    syntax_tree = pyjsparser.parse(script)
    elements = syntax_tree['body'][0]['declarations'][0]['init']['elements']
    if elements[13]['value'] != '':
        if float(elements[13]['value']) / float(elements[4]['value']) < 0.15:
            element_status = "מעט"
        else:
            element_status = "פנוי"
        parking_lot_info = {
            'Name': elements[0]['value'],
            'CentralParkCode': int(elements[3]['raw']),
            'GPSLattitude': "%.4f" % elements[1]['value'],
            'GPSLongitude': "%.4f" % elements[2]['value'],
            'capacity': elements[4]['value'],
            'address': elements[6]['value'] + " ," + elements[5]['value'],
            'InformationToShow': element_status,
            'free parking left': elements[13]['value']
        }
    return parking_lot_info


# when stating the app to get all the parking lots information
def get_parking_list():
    soup = BeautifulSoup(requests.get(PARKING_LIST_URL).content, features="html.parser")
    status = soup.find(class_="inner_list")
    city_names = status.findAll("div", class_="area_head")
    all_parking_list = soup.find(class_="area_parking_list")
    parking_lots_TLV = []
    for i in city_names:
        if i.findChild("div").contents[0].strip() == "תל-אביב יפו":
            nextSiblings = all_parking_list.find_next_siblings("div", class_="area_parking_list")
            li_tags = nextSiblings[1].find_all("li")
            for tag in li_tags:
                name = tag.text.strip()
                if name != "פארק צ'רלס קלור" and name != "מזאה" and name != "White City" and name != "רובע לב העיר" and name != "מגדל מאייר":
                    parking_lots_TLV.append(tag.text.strip())
    # calling the part where we get all the info of all parking lots
    all_parking_info = []
    for parking in parking_lots_TLV:
        parking_info = get_parking_lot_info(parking)
        if parking_info != {}:
            all_parking_info.append(parking_info)
    return all_parking_info
    # return parking_lots_TLV


# @functools.lru_cache(maxsize=None)
# async def get_parking_lot_status(parking_name):
#     PARKING_LOT_URL = f'https://centralpark.co.il/parking/{parking_name}/'
#     async with aiohttp.ClientSession() as session:
#         async with session.get(PARKING_LOT_URL) as response:
#             soup = BeautifulSoup(await response.text(), 'html.parser')
#             status = soup.find('div', class_='wrap_parking_detailes')
#             script = status.findChild('script').text.strip()
#             syntax_tree = slimit.astjs.parse(script)
#             elements = syntax_tree.body[0].declarations[0].init.elements
#             if elements[13].value != '':
#                 if float(elements[13].value) / float(elements[4].value) < 0.15:
#                     return 'מעט'
#                 else:
#                     return 'פנוי'
#             else:
#                 return 'Unknown'
#
#
# async def update_parking_lot_status(parking):
#     parking_name = parking[0]['Name']
#     information_to_show = await get_parking_lot_status(parking_name)
#     parking[0]['InformationToShow'] = information_to_show
#     return parking


def update_parking_lot_status(parking):
    parking_name = parking[0]['Name']
    PARKING_LOT_URL = f'https://centralpark.co.il/parking/{parking_name}/'
    soup = BeautifulSoup(requests.get(PARKING_LOT_URL).content, features="html.parser")
    status = soup.find("div", class_="wrap_parking_detailes")
    script = status.findChild("script").text.strip()
    syntax_tree = pyjsparser.parse(script)
    elements = syntax_tree['body'][0]['declarations'][0]['init']['elements']
    if elements[13]['value'] != '':
        if float(elements[13]['value']) / float(elements[4]['value']) < 0.15:
            parking[0]['InformationToShow'] = "מעט"
        else:
            parking[0]['InformationToShow'] = "פנוי"
    return parking


def get_all_parking_lots_information_updated(parking_list):
    all_parking_info = []
    for parking in parking_list:
        # calling to a function that update the status one parking lot
        parking_info = update_parking_lot_status(parking)
        all_parking_info.append(parking_info)
    return all_parking_info


def get_available_parking_lots(parking_list):
    available_parking_lots_TLV = []
    for parking in parking_list:
        if parking['InformationToShow'] == "פנוי":
            available_parking_lots_TLV.append(parking)
    return available_parking_lots_TLV


def get_few_available_parking_lots(parking_list):
    available_parking_lots_TLV = []
    for parking in parking_list:
        if parking['InformationToShow'] == "מעט":
            available_parking_lots_TLV.append(parking)
    return available_parking_lots_TLV


def update_status(parking_list):
    updated_parking_lots_TLV = []
    for parking in parking_list:
        if parking['InformationToShow'] == "פנוי":
            if float(parking['free parking left']) / float(parking_list['capacity']) < 0.15:
                parking['InformationToShow'] = "מעט"
            updated_parking_lots_TLV.append(parking)
    return updated_parking_lots_TLV


def get_closest_parking_by_address(parking_list_tlv, address):
    latitude, longitude = get_gps_coordinates(address)
    closest_places = find_closest_places(parking_list_tlv, latitude, longitude)
    #maybe remove the update from here
    #available_places = get_all_parking_lots_information_updated(closest_places)
    return closest_places


def get_closest_parking_by_distance(closest_places, distance):
    closest_parkingLots_by_d = [t for t in closest_places if t[1] <= distance]
    return closest_parkingLots_by_d


def get_duration_in_minutes(duration_str):
    # Split the duration string into hours and minutes
    parts = duration_str.split()
    hours = 0
    minutes = 0
    for i, part in enumerate(parts):
        if part == 'hour' or part == 'hours':
            hours = int(parts[i-1])
        elif part == 'min' or part == 'mins':
            minutes = int(parts[i-1])
    # Convert the duration to minutes
    total_minutes = hours * 60 + minutes
    return total_minutes


def get_closest_parking_by_duration(closest_places, duration):
    closest_parkingLots_by_drn = []
    duration_arr = duration.split()
    for parking_lot in closest_places:
        parking_lot_arr = parking_lot[2].split()
        if len(parking_lot_arr) == 2 and len(duration_arr) == 2:
            if int(parking_lot_arr[0]) <= int(duration_arr[0]):
                closest_parkingLots_by_drn.append(parking_lot)
        if len(parking_lot_arr) == 4 and len(duration_arr) == 4:
            if int(parking_lot_arr[0]) <= int(duration_arr[0]) and int(parking_lot_arr[2]) <= int(duration_arr[2]):
                closest_parkingLots_by_drn.append(parking_lot)
        if len(parking_lot_arr) == 2 and len(duration_arr) == 4:
            closest_parkingLots_by_drn.append(parking_lot)
        else:
            continue

    # Sort the list of tuples by duration in ascending order
    sorted_list = sorted(closest_parkingLots_by_drn, key=lambda x: get_duration_in_minutes(x[2]))

    return sorted_list


def main():
    parking_list_TLV = get_parking_list()
    closet_places = get_closest_parking_by_address(parking_list_TLV, "יבנה 30, תל אביב")
    print(closet_places)
    # closest_parkingLots_by_d = get_closest_parking_by_distance(closet_places, 500)
    # print(closest_parkingLots_by_d)
    closest_parkingLots_by_drn = get_closest_parking_by_duration(closet_places, '25 mins')
    print(closest_parkingLots_by_drn)


if __name__ == "__main__":
    # main('data', 'context')
    main()



# import base64
# import requests
# from urllib.parse import urlparse, parse_qs
# import re
# import pyjsparser
# from urllib.parse import urlparse, parse_qs
# from bs4 import BeautifulSoup
# from multiprocessing.dummy import Pool as ThreadPool
# import pandas as pd
# from datetime import datetime, timedelta, timezone
# import logging
# #from google.cloud import storage
# from pyarrow.feather import write_feather
# import pyarrow as pa
# from math import sin, cos, sqrt, atan2, radians
# import googlemaps
# import functools
#
# PARKING_LIST_URL = 'https://centralpark.co.il/רשימת-חניונים/'
# STATUS_TO_FLOAT = {'פנוי': 0, '': 1}
# ISRAEL_TZ = timezone(timedelta(hours=2))
# # Google Maps API key
# api_key = "AIzaSyA4DV1zbLCECX_kcZAWA4vCoti9Hm156W4"
#
#
# def get_gps_coordinates(hebrew_address):
#     # Set the API endpoint and your API key
#     endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
#
#     # Set the address and other parameters
#     params = {
#         "address": hebrew_address,
#         "key": api_key,
#         "language": "he"
#     }
#
#     # Make the API request
#     response = requests.get(endpoint, params=params)
#
#     # Get the latitude and longitude from the response
#     latitude = response.json()["results"][0]["geometry"]["location"]["lat"]
#     longitude = response.json()["results"][0]["geometry"]["location"]["lng"]
#
#     # Print the latitude and longitude
#     print(latitude)
#     print(longitude)
#
#     return latitude, longitude
#
#
# def find_closest_places(places, latitude, longitude):
#     # Replace YOUR_API_KEY with your actual API key
#     API_KEY = api_key
#     R = 6373.0
#
#     # Initialize a list to store the closest parking lots from each parking lot to the GPS coordinate
#     closest_places = []
#
#     # Loop through the list of places and calculate the distance from each place to the GPS coordinate
#     for place in places:
#         # Define the client object
#         gmaps = googlemaps.Client(api_key)
#
#         # Define the two points by latitude and longitude
#         point1 = (latitude, longitude)  # example point
#         point2 = (float(place['latitude']), float(place['longitude']))  # example point
#
#         # Define the transportation mode (walking)
#         mode = "walking"
#
#         # Define the departure time
#         departure_time = datetime.now()
#
#         # Call the directions API
#         result = gmaps.directions(point1, point2, mode=mode, departure_time=departure_time)
#
#         # Extract the distance in meters
#         distance_meters = result[0]['legs'][0]['distance']['value']
#
#         # Extract the duration
#         duration = result[0]['legs'][0]['duration']['text']
#         #int_duration = int(duration.split()[0])
#
#         closest_places.append((place, distance_meters, duration))
#
#     # Find the index of the minimum distance in the list
#     # min_index = distances.index(min(distances))
#     # sort the list of tuples by distance in ascending order
#     closest_places.sort(key=lambda x: x[1])
#     # print(closest_places)
#     # Return the name of the place with the minimum distance
#     return closest_places
#
#
# def get_parking_lot_info(parking_name):
#     PARKING_LOT_URL = f'https://centralpark.co.il/parking/{parking_name}/'
#     soup = BeautifulSoup(requests.get(PARKING_LOT_URL).content, features="html.parser")
#     status = soup.find("div", class_="wrap_parking_detailes")
#     script = status.findChild("script").text.strip()
#     syntax_tree = pyjsparser.parse(script)
#     elements = syntax_tree['body'][0]['declarations'][0]['init']['elements']
#     parking_lot_info = {
#         'Name': elements[0]['value'],
#         'CentralParkCode': int(elements[3]['raw']),
#         'latitude': "%.4f" % elements[1]['value'],
#         'longitude': "%.4f" % elements[2]['value'],
#         'capacity': elements[4]['value'],
#         'address': elements[6]['value'] + " ," + elements[5]['value'],
#         'InformationToShow': elements[12]['value'],
#         'free parking left': elements[13]['value']
#     }
#     return parking_lot_info
#
#
# def get_parking_list():
#     soup = BeautifulSoup(requests.get(PARKING_LIST_URL).content, features="html.parser")
#     status = soup.find(class_="inner_list")
#     city_names = status.findAll("div", class_="area_head")
#     all_parking_list = soup.find(class_="area_parking_list")
#     parking_lots_TLV = []
#     for i in city_names:
#         if i.findChild("div").contents[0].strip() == "תל-אביב יפו":
#             nextSiblings = all_parking_list.find_next_siblings("div", class_="area_parking_list")
#             li_tags = nextSiblings[1].find_all("li")
#             for tag in li_tags:
#                 name = tag.text.strip()
#                 if name != "פארק צ'רלס קלור" and name != "מזאה" and name != "White City" and name != "רובע לב העיר" and name != "מגדל מאייר":
#                     parking_lots_TLV.append(tag.text.strip())
#
#     # לא עדיף להכניס כבר לכאן את העידכון של הסטטוס של המעט? ואז לשלוח את זה כבר מוכן?
#     # updated_list = update_status(parking_lots_TLV)
#     return parking_lots_TLV
#
#
# def get_all_parking_lots_info(parking_list):
#     all_parking_info = []
#     for parking in parking_list:
#         parking_info = get_parking_lot_info(parking)
#         all_parking_info.append(parking_info)
#     return all_parking_info
#
#
# def get_available_parking_lots(parking_list):
#     available_parking_lots_TLV = []
#     for parking in parking_list:
#         if parking['InformationToShow'] == "פנוי":
#             available_parking_lots_TLV.append(parking)
#     return available_parking_lots_TLV
#
#
# def get_few_available_parking_lots(parking_list):
#     available_parking_lots_TLV = []
#     for parking in parking_list:
#         if parking['InformationToShow'] == "מעט":
#             available_parking_lots_TLV.append(parking)
#     return available_parking_lots_TLV
#
#
# def update_status(parking_list):
#     updated_parking_lots_TLV = []
#     for parking in parking_list:
#         if parking['InformationToShow'] == "פנוי":
#             if float(parking['free parking left']) / float(parking_list['capacity']) < 0.15:
#                 parking['InformationToShow'] = "מעט"
#             updated_parking_lots_TLV.append(parking)
#     return updated_parking_lots_TLV
#
#
# def get_closest_parking_by_address(parking_list_tlv, address):
#     available_places = get_all_parking_lots_info(parking_list_tlv)
#     latitude, longitude = get_gps_coordinates(address)
#     closest_places = find_closest_places(available_places, latitude, longitude)
#     return closest_places
#
#
# def get_closest_parking_by_distance(closest_places, distance):
#     closest_parkingLots_by_d = [t for t in closest_places if t[1] <= distance]
#     return closest_parkingLots_by_d
#
#
# def get_duration_in_minutes(duration_str):
#     # Split the duration string into hours and minutes
#     parts = duration_str.split()
#     hours = 0
#     minutes = 0
#     for i, part in enumerate(parts):
#         if part == 'hour' or part == 'hours':
#             hours = int(parts[i-1])
#         elif part == 'min' or part == 'mins':
#             minutes = int(parts[i-1])
#     # Convert the duration to minutes
#     total_minutes = hours * 60 + minutes
#     return total_minutes
#
#
# def get_closest_parking_by_duration(closest_places, duration):
#     closest_parkingLots_by_drn = []
#     duration_arr = duration.split()
#     for parking_lot in closest_places:
#         parking_lot_arr = parking_lot[2].split()
#         if len(parking_lot_arr) == 2 and len(duration_arr) == 2:
#             if int(parking_lot_arr[0]) <= int(duration_arr[0]):
#                 closest_parkingLots_by_drn.append(parking_lot)
#         if len(parking_lot_arr) == 4 and len(duration_arr) == 4:
#             if int(parking_lot_arr[0]) <= int(duration_arr[0]) and int(parking_lot_arr[2]) <= int(duration_arr[2]):
#                 closest_parkingLots_by_drn.append(parking_lot)
#         if len(parking_lot_arr) == 2 and len(duration_arr) == 4:
#             closest_parkingLots_by_drn.append(parking_lot)
#         else:
#             continue
#
#     # Sort the list of tuples by duration in ascending order
#     sorted_list = sorted(closest_parkingLots_by_drn, key=lambda x: get_duration_in_minutes(x[2]))
#
#     return sorted_list
#
#
# def main():
#     parking_list_TLV = get_parking_list()
#     #print(parking_list_TLV)
#     print(get_all_parking_lots_info(parking_list_TLV))
#     # closet_places = get_closest_parking_by_address(parking_list_TLV, "הברזל 10, תל אביב")
#     # print(closet_places)
#     # # closest_parkingLots_by_d = get_closest_parking_by_distance(closet_places, 500)
#     # # print(closest_parkingLots_by_d)
#     # closest_parkingLots_by_drn = get_closest_parking_by_duration(closet_places, '25 mins')
#     # print(closest_parkingLots_by_drn)
#
#
# if __name__ == "__main__":
#     # main('data', 'context')
#     main()