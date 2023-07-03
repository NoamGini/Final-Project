from backend.src.mongoDB import *
import requests
import pyjsparser
from datetime import datetime
import googlemaps
from bs4 import BeautifulSoup
from backend.constants import *


def get_gps_coordinates(hebrew_address):
    # Set the API endpoint and your API key
    endpoint = GOOGLE_ENDPOINT

    # Set the address and other parameters
    params = {
        ADDRESS2: hebrew_address,
        KEY: GOOGLE_MAPS_API_KEY,
        LANGUAGE: HEBREW
    }

    # Make the API request
    response = requests.get(endpoint, params=params)
    # Get the latitude and longitude from the response
    latitude = response.json()[RESULTS][0][GEOMETRY][LOCATION][LATITUDE]
    longitude = response.json()[RESULTS][0][GEOMETRY][LOCATION][LONGITUDE]

    return latitude, longitude


def find_closest_places(places, latitude, longitude):
    # Initialize a list to store the closest parking lots from each parking lot to the GPS coordinate
    closest_places = []

    # Loop through the list of places and calculate the distance from each place to the GPS coordinate
    for place in places:
        # Define the client object
        gmaps = googlemaps.Client(GOOGLE_MAPS_API_KEY)
        # Define the two points by latitude and longitude
        point1 = (latitude, longitude)  # example point
        point2 = (float(place[PARKING_GPS_LAT]), float(place[PARKING_GPS_LON]))  # example point
        # Define the transportation mode (walking)
        mode = WALKING
        # Define the departure time
        departure_time = datetime.now()
        # Call the directions API
        result = gmaps.directions(point1, point2, mode=mode, departure_time=departure_time)
        # Extract the distance in meters
        distance_meters = result[0][LAGS][0][DISTANCE][VALUE]
        # Extract the duration
        duration = result[0][LAGS][0][DURATION][TEXT]
        # int_duration = int(duration.split()[0])
        closest_places.append((place, distance_meters, duration))
        # If we have found 10 places, break out of the loop
        if len(closest_places) == 10:
            break

    closest_places.sort(key=lambda x: x[1])
    return closest_places


def get_parking_lot_info(parking_name):
    parking_lot_info = {}
    PARKING_LOT_URL = CENTRAL_URL + f'{parking_name}/'
    soup = BeautifulSoup(requests.get(PARKING_LOT_URL).content, features=HTML_PARSER)
    status = soup.find(DIV, class_=CLASS_WRAP_PARK_DETAILS)
    script = status.findChild(SCRIPT).text.strip()
    syntax_tree = pyjsparser.parse(script)
    elements = syntax_tree[BODY][0][DECLARATIONS][0][INIT][ELEMENTS]

    if elements[13][VALUE] != EMPTY:
        if float(elements[13][VALUE]) / float(elements[4][VALUE]) < 0.15:
            element_status = STATUSES[2]
        else:
            element_status = STATUSES[0]
        parking_lot_info = {
            NAME: elements[0][VALUE],
            PARKING_CENTRAL_CODE: int(elements[3][RAW]),
            PARKING_GPS_LAT: FLOATING_POINT_FORMAT % elements[1][VALUE],
            PARKING_GPS_LON: FLOATING_POINT_FORMAT % elements[2][VALUE],
            CAPACITY: elements[4][VALUE],
            ADDRESS2: elements[6][VALUE] + COMMA + elements[5][VALUE],
            INFO_TO_SHOW: element_status,
            FREE_PARKING_LEFT: elements[13][VALUE]
        }

    return parking_lot_info


# when stating the app to get all the parking lots information
def get_parking_list():
    soup = BeautifulSoup(requests.get(PARKING_LIST_URL).content, features=HTML_PARSER)
    status = soup.find(class_=CLASS_INNER_LIST)
    city_names = status.findAll(DIV, class_=CLASS_AREA_HEAD)
    all_parking_list = soup.find(class_=CLASS_AREA_PARK_LIST)
    parking_lots_TLV = []

    for i in city_names:
        if i.findChild(DIV).contents[0].strip() == TLV:
            nextSiblings = all_parking_list.find_next_siblings(DIV, class_=CLASS_AREA_PARK_LIST)
            li_tags = nextSiblings[1].find_all(LI)
            parking_lots_TLV = [tag.text.strip() for tag in li_tags if tag.text.strip() not in ADDRESSES_TO_DISMISS]

    # calling the part where we get all the info of all parking lots
    all_parking_info = []
    for parking in parking_lots_TLV:
        parking_info = get_parking_lot_info(parking)
        if parking_info != {}:
            all_parking_info.append(parking_info)

    return all_parking_info


def update_parking_lot_status(parking):
    parking_name = parking[0][NAME]
    PARKING_LOT_URL = CENTRAL_URL + f'{parking_name}/'
    soup = BeautifulSoup(requests.get(PARKING_LOT_URL).content, features=HTML_PARSER)
    status = soup.find(DIV, class_=CLASS_WRAP_PARK_DETAILS)
    script = status.findChild(SCRIPT).text.strip()
    syntax_tree = pyjsparser.parse(script)
    elements = syntax_tree[BODY][0][DECLARATIONS][0][INIT][ELEMENTS]

    if elements[13][VALUE] != EMPTY:
        if float(elements[13][VALUE]) / float(elements[4][VALUE]) < UPPER_BOUND:
            parking[0][INFO_TO_SHOW] = STATUSES[2]
        else:
            parking[0][INFO_TO_SHOW] = STATUSES[0]

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
        if parking[INFO_TO_SHOW] == STATUSES[0]:
            available_parking_lots_TLV.append(parking)

    return available_parking_lots_TLV


def get_few_available_parking_lots(parking_list):
    available_parking_lots_TLV = []

    for parking in parking_list:
        if parking[INFO_TO_SHOW] == STATUSES[2]:
            available_parking_lots_TLV.append(parking)

    return available_parking_lots_TLV


def update_status(parking_list):
    updated_parking_lots_TLV = []

    for parking in parking_list:
        if parking[INFO_TO_SHOW] == STATUSES[0]:
            if float(parking[FREE_PARKING_LEFT]) / float(parking_list[CAPACITY]) < UPPER_BOUND:
                parking[INFO_TO_SHOW] = STATUSES[2]
            updated_parking_lots_TLV.append(parking)

    return updated_parking_lots_TLV


def get_closest_parking_by_address(parking_list_tlv, address):
    latitude, longitude = get_gps_coordinates(address)
    closest_places = find_closest_places(parking_list_tlv, latitude, longitude)
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
        if part == TIMES[0] or part == TIMES[1]:
            hours = int(parts[i - 1])
        elif part == TIMES[2] or part == TIMES[3]:
            minutes = int(parts[i - 1])

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
