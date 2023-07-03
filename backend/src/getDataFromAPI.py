from datetime import datetime
from zeep import Client
import requests
import googlemaps
from backend.constants import *

client = Client(wsdl=WSDL)


# return all parking statuses
# info - AhuzotCode': 81,
# 'Name': 'רידינג מזרח',
# 'InformationToShow': 'פנוי',
# 'LastUpdateFromDambach': datetime.datetime(2023, 3, 22, 13, 16, 39, 317000),
def get_all_lots_status():
    all_parking_lots_status = client.service.GetAllCarParkStatus(API_HAUZOT_USERNAME, API_HAUZOT_PASSWORD, TFAULT,
                                                                 FWS_PWD)
    return all_parking_lots_status[GET_ALL_DETAILS][GET_CAR_PARK_DYNAMIC_DETAILS]


# get all available parking lots - represented as: {
# 'AhuzotCode': 81,
# 'Name': 'רידינג מזרח',
# 'InformationToShow': 'פנוי',
# 'LastUpdateFromDambach': datetime.datetime(2023, 3, 22, 13, 4, 39, 387000)}
def all_free_parking_lots():
    all_parking_lots_status = client.service.GetAllCarParkStatus(API_HAUZOT_USERNAME, API_HAUZOT_PASSWORD, TFAULT,
                                                                 FWS_PWD)
    all_parking_lots_status_array = all_parking_lots_status[GET_ALL_DETAILS][GET_CAR_PARK_DYNAMIC_DETAILS]
    all_free_parking_lots_array = []
    for parking_lot in all_parking_lots_status_array:
        # "    " or "סגור" - meaning the parking lot is closed
        # there is only 60 with real time status - "סגור" appease 3 times "    " = appease 8 times
        if parking_lot[INFO_TO_SHOW] == STATUSES[0]:
            all_free_parking_lots_array.append(parking_lot)
    all_free_parking_lots_info = get_parking_list_info(all_free_parking_lots_array)
    return all_free_parking_lots_info


def all_few_parking_lots_left():
    all_parking_lots_status = client.service.GetAllCarParkStatus(API_HAUZOT_USERNAME, API_HAUZOT_PASSWORD, TFAULT,
                                                                 FWS_PWD)
    all_parking_lots_status_array = all_parking_lots_status[GET_ALL_DETAILS][GET_CAR_PARK_DYNAMIC_DETAILS]
    all_free_parking_lots_array = []
    for parking_lot in all_parking_lots_status_array:
        # "    " or "סגור" - meaning the parking lot is closed
        # there is only 60 with real time status - "סגור" appease 3 times "    " = appease 8 times
        if parking_lot[INFO_TO_SHOW] == STATUSES[2]:
            all_free_parking_lots_array.append(parking_lot)
    all_free_parking_lots_info = get_parking_list_info(all_free_parking_lots_array)
    return all_free_parking_lots_info


# info :{'AhuzotCode': 10, 'Name': 'בזל', 'Address': 'אשתורי הפרחי 5 תל-אביב יפו', 'GPSLattitude': Decimal('32.0898'),
# 'GPSLongitude': Decimal('34.7798')}
def get_parking_lot_location_details(ahuzot_code):
    parking_lot_details = client.service.GetCarParkDetails(ahuzot_code, API_HAUZOT_USERNAME, API_HAUZOT_PASSWORD,
                                                           TFAULT, FWS_PWD)
    parking_lot_details_dict = parking_lot_details[GET_CAR_PARK_STATIC_DETAILS]
    parking_lot_location = {k: parking_lot_details_dict[k] for k in
                            (PARKING_AHUZOT_CODE, NAME, ADDRESS, PARKING_GPS_LAT,
                             PARKING_GPS_LON)}

    if parking_lot_location[ADDRESS] == ADDRESSES_TO_CHANGE[0]:
        parking_lot_location[ADDRESS] = UPDATED_ADDRESSES[0]

    if parking_lot_location[NAME] == ADDRESSES_TO_CHANGE[1]:
        parking_lot_location[ADDRESS] = UPDATED_ADDRESSES[1]

    if parking_lot_location[NAME] == ADDRESSES_TO_CHANGE[2]:
        parking_lot_location[ADDRESS] = UPDATED_ADDRESSES[2]

    if parking_lot_location[NAME] == ADDRESSES_TO_CHANGE[3]:
        parking_lot_location[ADDRESS] = UPDATED_ADDRESSES[3]

    lat, lon = get_gps_coordinates(parking_lot_location[ADDRESS])
    parking_lot_location[PARKING_GPS_LAT] = lat
    parking_lot_location[PARKING_GPS_LON] = lon

    return parking_lot_location


# returns "פנוי" / "מעט" / "מלא"
def get_parking_lot_status(ahuzot_code):
    CarParkingStatus = client.service.GetCarParkStatus(ahuzot_code, API_HAUZOT_USERNAME, API_HAUZOT_PASSWORD, TFAULT,
                                                       FWS_PWD)
    CarParkingStatusData = CarParkingStatus[GET_CAR_PARK_STATUS_RES]
    status = CarParkingStatusData[INFO_TO_SHOW]
    return status


def update_status(info, code):
    status = get_parking_lot_status(code)
    info[INFO_TO_SHOW] = status
    return info


def get_all_parking_lots_info_hauzot():
    places = get_all_lots_status()
    places_info = get_parking_list_info(places)
    return places_info


# function that returns parking info:
# {'AhuzotCode': 10, 'Name': 'בזל', 'Address': 'אשתורי הפרחי 5 תל-אביב יפו', 'GPSLattitude': Decimal('32.0898'),
# 'GPSLongitude': Decimal('34.7798'), 'InformationToShow': 'פנוי'}
def get_parking_list_info(parking_list):
    parking_list_info = []
    for i in parking_list:
        if i[INFO_TO_SHOW] == STATUS_UNAVAILABLE:
            continue
        code = (i[PARKING_AHUZOT_CODE])
        info = get_parking_lot_location_details(code)
        updated_info = update_status(info, code)
        parking_list_info.append(updated_info)

    return parking_list_info


# convert address to GPS coordinates
def get_gps_coordinates(hebrew_address):
    # Set the API endpoint
    endpoint = GOOGLE_ENDPOINT

    params = {
        ADDRESS_SMALL_LETTER: hebrew_address,
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

        closest_places.append((place, distance_meters, duration))
        # If we have found 10 places, break out of the loop
        if len(closest_places) == 10:
            break

    closest_places.sort(key=lambda x: x[1])
    # print(closest_places)
    # Return the name of the place with the minimum distance
    return closest_places


def get_closest_parking_by_address_hauzot(places_info, address):
    latitude, longitude = get_gps_coordinates(address)
    closest_places = find_closest_places(places_info, latitude, longitude)
    return closest_places


def get_closest_parking_by_distance_hauzot(closest_places, distance):
    closest_parkingLots_by_d = [t for t in closest_places if t[1] <= int(distance)]
    return closest_parkingLots_by_d


# the function gets parking name and returns its details else return Not Found
# info - {'AhuzotCode': 14, 'Name': 'ברוריה', 'Address': 'יגאל אלון 151 תל-אביב יפו',
# 'GPSLattitude': Decimal('32.0781'),
# 'GPSLongitude': Decimal('34.7969'), '
def get_parking_info_by_name(name):
    all_lots = get_all_lots_status()
    for i in all_lots:
        if i[NAME] == name:
            parking_info = get_parking_lot_location_details(i[PARKING_AHUZOT_CODE])
            updated_parking_info = update_status(parking_info, i[PARKING_AHUZOT_CODE])
            return updated_parking_info
    return None
