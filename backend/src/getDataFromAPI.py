from datetime import datetime
from numpy import double
from zeep import Client
import requests
from decimal import Decimal
import json
import googlemaps


username = "wsu-noaziv"
user_password = "N0@z!u386"
tFault = "OK"
fWSPwd = "10fd90e7004c6499fe86146fc888eee62c2d1e1ae0bf7a1c34c3346cec15fada"
# Google Maps API key
#api_key= "AIzaSyBmzgNX44L4plhmf4j5BFnUtfHmIWnD9Ts"
api_key='AIzaSyDGG3PgHwpThGyw-BeKsaTs3mS5eS3BZXE'
#api_key ="AIzaSyDKupYcq3t0hyHTn-YQRriH57ch-Ekw0cs"
# api_key = "AIzaSyA4DV1zbLCECX_kcZAWA4vCoti9Hm156W4"
client = Client(wsdl='http://parkinfo.ahuzot.co.il/cp.asmx?wsdl')


#return all parking statuses
#info - AhuzotCode': 81,
    # 'Name': 'רידינג מזרח',
    # 'InformationToShow': 'פנוי',
    # 'LastUpdateFromDambach': datetime.datetime(2023, 3, 22, 13, 16, 39, 317000),
def get_all_lots_status():
    all_parking_lots_status = client.service.GetAllCarParkStatus(username, user_password, tFault, fWSPwd)
    return all_parking_lots_status['GetAllCarParkStatusResult']['CarParkDynamicDetails']


#get all available parking lots - represented as: {
    # 'AhuzotCode': 81,
    # 'Name': 'רידינג מזרח',
    # 'InformationToShow': 'פנוי',
    # 'LastUpdateFromDambach': datetime.datetime(2023, 3, 22, 13, 4, 39, 387000)}
def all_free_parking_lots():
    all_parking_lots_status = client.service.GetAllCarParkStatus(username, user_password, tFault, fWSPwd)
    all_parking_lots_status_array = all_parking_lots_status['GetAllCarParkStatusResult']['CarParkDynamicDetails']
    all_free_parking_lots_array = []
    for parking_lot in all_parking_lots_status_array:
        # "    " or "סגור" - meaning the parking lot is closed
        # there is only 60 with real time status - "סגור" appease 3 times "    " = appease 8 times
        if parking_lot['InformationToShow'] == "פנוי":
            all_free_parking_lots_array.append(parking_lot)
    # print(all_free_parking_lots_array)
    all_free_parking_lots_info = get_parking_list_info(all_free_parking_lots_array)
    return all_free_parking_lots_info


def all_few_parking_lots_left():
    all_parking_lots_status = client.service.GetAllCarParkStatus(username, user_password, tFault, fWSPwd)
    all_parking_lots_status_array = all_parking_lots_status['GetAllCarParkStatusResult']['CarParkDynamicDetails']
    all_free_parking_lots_array = []
    for parking_lot in all_parking_lots_status_array:
        # "    " or "סגור" - meaning the parking lot is closed
        # there is only 60 with real time status - "סגור" appease 3 times "    " = appease 8 times
        if parking_lot['InformationToShow'] == "מעט":
            all_free_parking_lots_array.append(parking_lot)
    all_free_parking_lots_info = get_parking_list_info(all_free_parking_lots_array)
    return all_free_parking_lots_info


#info :{'AhuzotCode': 10, 'Name': 'בזל', 'Address': 'אשתורי הפרחי 5 תל-אביב יפו', 'GPSLattitude': Decimal('32.0898'),
# 'GPSLongitude': Decimal('34.7798')}
def get_parking_lot_location_details(ahuzot_code):
    parking_lot_details = client.service.GetCarParkDetails(ahuzot_code, username, user_password, tFault, fWSPwd)
    parking_lot_details_dict = parking_lot_details['GetCarParkDetailsResult']
    parking_lot_location = {k: parking_lot_details_dict[k] for k in ('AhuzotCode','Name', 'Address', 'GPSLattitude',
                                                                'GPSLongitude')}

    if parking_lot_location['Address'] == 'שבט בנימין 1':
        parking_lot_location['Address'] = 'שבט בנימין 1 תל אביב יפו'

    if parking_lot_location['Name'] == 'כרמל 2 ':
        parking_lot_location['Address'] = 'סמטת הכרמל 12 תל אביב'

    if parking_lot_location['Name'] == 'רידינג מערב':
        parking_lot_location['Address'] = 'רוקח 7 תל-אביב יפו'

    if parking_lot_location['Name'] == 'רידינג מזרח':
        parking_lot_location['Address'] = 'רוקח 15 תל-אביב יפו'

    lat, lon = get_gps_coordinates(parking_lot_location['Address'])
    parking_lot_location['GPSLattitude'] = lat
    parking_lot_location['GPSLongitude'] = lon

    return parking_lot_location


#returns "פנוי" / "מעט" / "מלא"
def get_parking_lot_status(ahuzot_code):
    CarParkingStatus = client.service.GetCarParkStatus(ahuzot_code, username, user_password, tFault, fWSPwd)
    CarParkingStatusData = CarParkingStatus['GetCarParkStatusResult']
    status = CarParkingStatusData['InformationToShow']
    return status


def update_status(info, code):
    status = get_parking_lot_status(code)
    info['InformationToShow'] = status
    return info


def get_all_parking_lots_info_hauzot():
    places = get_all_lots_status()
    places_info = get_parking_list_info(places)
    return places_info

# function that returns parking info:
#{'AhuzotCode': 10, 'Name': 'בזל', 'Address': 'אשתורי הפרחי 5 תל-אביב יפו', 'GPSLattitude': Decimal('32.0898'),
# 'GPSLongitude': Decimal('34.7798'), 'InformationToShow': 'פנוי'}
def get_parking_list_info(parking_list):
    parking_list_info = []
    for i in parking_list:
        if i['InformationToShow'] == '    ':
            print("found empty status")
            continue
        code = (i['AhuzotCode'])
        info = get_parking_lot_location_details(code)
        updated_info = update_status(info, code)
        # status = get_parking_lot_status(code)
        # info['InformationToShow']= status
        # info.append({'InformationToShow': status})
        parking_list_info.append(updated_info)

    return parking_list_info


# convert address to GPS coordinates
def get_gps_coordinates(hebrew_address):
    # Set the API endpoint and your API key
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
    #print(hebrew_address)
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

    return latitude, longitude


def find_closest_places(places, latitude, longitude):
    # Replace YOUR_API_KEY with your actual API key
    API_KEY = api_key
    R = 6373.0

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
        #float_duration = int(duration.split()[0])

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


def get_closest_parking_by_address_hauzot(places_info, address):
   # places = get_all_lots_status()
    #places = all_free_parking_lots()
    #places_info = get_parking_list_info(places)
    latitude, longitude = get_gps_coordinates(address)
    closest_places = find_closest_places(places_info, latitude, longitude)
   #update statuses
   #maybe remove the update from here
    # for parking in closest_places:
    #     update_status(parking[0], parking[0]['AhuzotCode'])
    return closest_places


def get_closest_parking_by_distance_hauzot(closest_places, distance):
    closest_parkingLots_by_d = [t for t in closest_places if t[1] <= int(distance)]
    return closest_parkingLots_by_d


#the function gets parking name and returns its details else return Not Found
#info - {'AhuzotCode': 14, 'Name': 'ברוריה', 'Address': 'יגאל אלון 151 תל-אביב יפו', 'GPSLattitude': Decimal('32.0781'),
# 'GPSLongitude': Decimal('34.7969'), '
def get_parking_info_by_name(name):
    all_lots = get_all_lots_status()
    for i in all_lots:
        if i['Name'] == name:
            parking_info = get_parking_lot_location_details(i['AhuzotCode'])
            updated_parking_info = update_status(parking_info, i['AhuzotCode'])
            return updated_parking_info
    return None
