import googlemaps
from backend.constants import *



def create_parking_database(starting_point, num_parkings):

    # Initialize the Google Maps client
    gmaps = googlemaps.Client(GOOGLE_MAPS_API_KEY)

    # Initialize the database
    generated_list = []

    street_num = starting_point.split(",")[0]
    city = starting_point.split(",")[1]
    street = street_num.split(" ")[0] + " " + street_num.split(" ")[1]
    num = int(street_num.split(" ")[2])

    for i in range(num_parkings):

        address = f'{street} {num},{city}'
        # address = f'{starting_point.split(",")[0].split(" ")[0]+starting_point.split(",")[0].split(" ")[1]} {i+2}, {starting_point.split(",")[1]}'

        # Retrieve coordinates for the current address
        geocode_result = gmaps.geocode(address)
        if geocode_result:
            latitude = geocode_result[0][GEOMETRY][LOCATION][LATITUDE]
            longitude = geocode_result[0][GEOMETRY][LOCATION][LONGITUDE]
        else:
            raise ValueError(INVALID_ADDRESS + f'{address}')

        # Create the parking entry
        parking = {
            ADDRESS2: address,
            KL_LATITUDE: latitude,
            KL_LONGITUDE: longitude,
            RELEASE_TIME: EMPTY,
            STATUS: STATUSES[3],
            HIDDEN: True
        }

        # Add the parking to the list
        generated_list.append(parking)
        num += 2

    return generated_list


def get_parking_kahol_lavan_list(parking_kahol_lavan_list):
    parking1 = {ADDRESS2: 'אשתורי הפרחי 12, תל אביב', KL_LATITUDE: 32.0896975, KL_LONGITUDE: 34.780284,
                RELEASE_TIME: EMPTY, STATUS: STATUSES[0], HIDDEN: False}

    parking2 = {ADDRESS2: 'דב הוז 5, תל אביב', KL_LATITUDE: 32.0797165, KL_LONGITUDE: 34.7721574,
                RELEASE_TIME: EMPTY, STATUS: STATUSES[0], HIDDEN: False}

    parking3 = {ADDRESS2: 'שדרות היוצר 11, תל אביב', KL_LATITUDE: 32.0892596, KL_LONGITUDE: 34.7796131,
                RELEASE_TIME: EMPTY, STATUS: STATUSES[0], HIDDEN: False}

    parking4 = {ADDRESS2: 'הכובשים 43, תל אביב', KL_LATITUDE: 32.0695758, KL_LONGITUDE: 34.7662558,
                RELEASE_TIME: EMPTY, STATUS: STATUSES[0], HIDDEN: False}

    parking5 = {ADDRESS2: 'חובבי ציון 10, תל אביב', KL_LATITUDE: 32.0750460, KL_LONGITUDE: 34.7690299,
                RELEASE_TIME: EMPTY, STATUS: STATUSES[0], HIDDEN: False}

    parking6 = {ADDRESS2: 'לילינבלום 4, תל אביב', KL_LATITUDE: 32.0617856, KL_LONGITUDE: 34.7675207,
                RELEASE_TIME: EMPTY, STATUS: STATUSES[0], HIDDEN: False}

    parking7 = {ADDRESS2: 'חובבי ציון 3, תל אביב', KL_LATITUDE: 32.0744155, KL_LONGITUDE: 34.7686057,
                RELEASE_TIME: EMPTY, STATUS: STATUSES[0], HIDDEN: False}

    parking8 = {ADDRESS2: 'בן עמי 12, תל אביב', KL_LATITUDE: 32.0784095, KL_LONGITUDE: 34.7729590,
                RELEASE_TIME: EMPTY, STATUS: STATUSES[0], HIDDEN: False}

    parking9 = {ADDRESS2: 'המרד 36, תל אביב', KL_LATITUDE: 32.0645403, KL_LONGITUDE: 34.7648474,
                RELEASE_TIME: EMPTY, STATUS: STATUSES[0], HIDDEN: False}

    parking10 = {ADDRESS2: 'לילינבלום 14, תל אביב', KL_LATITUDE: 32.0619556, KL_LONGITUDE: 34.7686573,
                 RELEASE_TIME: "09:50", STATUS: STATUSES[4], HIDDEN: False}

    parking11 = {ADDRESS2: 'מחנה יוסף 34, תל אביב', KL_LATITUDE: 32.0645131, KL_LONGITUDE: 34.7667812,
                 RELEASE_TIME: EMPTY, STATUS: STATUSES[3], HIDDEN: True}

    parking12 = {ADDRESS2: 'דגניה 3, תל אביב', KL_LATITUDE: 32.0629708, KL_LONGITUDE: 34.7647325,
                 RELEASE_TIME: EMPTY, STATUS: STATUSES[0], HIDDEN: False}

    parking_kahol_lavan_list.append(parking1)
    parking_kahol_lavan_list.append(parking2)
    parking_kahol_lavan_list.append(parking3)
    parking_kahol_lavan_list.append(parking4)
    parking_kahol_lavan_list.append(parking5)
    parking_kahol_lavan_list.append(parking6)
    parking_kahol_lavan_list.append(parking7)
    parking_kahol_lavan_list.append(parking8)
    parking_kahol_lavan_list.append(parking9)
    parking_kahol_lavan_list.append(parking10)
    parking_kahol_lavan_list.append(parking11)
    parking_kahol_lavan_list.append(parking12)

    return parking_kahol_lavan_list


def generate_list_kahol_lavan():
    parking_kahol_lavan_list = []
    starting_points = STARTING_POINTS
    num_parkings = 50

    parking_kahol_lavan_list = get_parking_kahol_lavan_list(parking_kahol_lavan_list)

    for i in range(len(starting_points)):
        starting_point = starting_points[i]
        parking_kahol_lavan_list += create_parking_database(starting_point, num_parkings)

    return parking_kahol_lavan_list


def main():
    parking_kahol_lavan_list = generate_list_kahol_lavan()
    # Print the parking list
    for parking in parking_kahol_lavan_list:
        print(parking)


if __name__ == '__main__':
    main()
