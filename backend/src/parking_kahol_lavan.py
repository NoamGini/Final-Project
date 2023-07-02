import googlemaps
api_key = 'AIzaSyDGG3PgHwpThGyw-BeKsaTs3mS5eS3BZXE'


def create_parking_database(starting_point, num_parkings):
    # Initialize the Google Maps client
    gmaps = googlemaps.Client(api_key)

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
            latitude = geocode_result[0]['geometry']['location']['lat']
            longitude = geocode_result[0]['geometry']['location']['lng']
        else:
            raise ValueError(f'Invalid address: {address}')

        # Create the parking entry
        parking = {
            'address': address,
            'latitude': latitude,
            'longitude': longitude,
            'release_time': '',
            'status': 'תפוס',
            'hidden': True
        }

        # Add the parking to the list
        generated_list.append(parking)
        num += 2

    return generated_list


def get_parking_kahol_lavan_list(parking_kahol_lavan_list):
    parking1 = {'address': 'אשתורי הפרחי 12, תל אביב', 'latitude': 32.0896975, 'longitude': 34.780284,
                'release_time': "", 'status': 'פנוי', 'hidden': False}

    parking2 = {'address': 'דב הוז 5, תל אביב', 'latitude': 32.0797165, 'longitude': 34.7721574,
                'release_time': "", 'status': 'פנוי', 'hidden': False}

    parking3 = {'address': 'שדרות היוצר 11, תל אביב', 'latitude': 32.0892596, 'longitude': 34.7796131,
                'release_time': "", 'status': 'פנוי', 'hidden': False}

    parking4 = {'address': 'הכובשים 43, תל אביב', 'latitude': 32.0695758, 'longitude': 34.7662558, 'release_time': "",
                'status': 'פנוי', 'hidden': False}

    parking5 = {'address': 'חובבי ציון 10, תל אביב', 'latitude': 32.0750460, 'longitude': 34.7690299,
                'release_time': "", 'status': 'פנוי', 'hidden': False}

    parking6 = {'address': 'לילינבלום 4, תל אביב', 'latitude': 32.0617856, 'longitude': 34.7675207, 'release_time': "",
                'status': 'פנוי', 'hidden': False}

    parking7 = {'address': 'חובבי ציון 3, תל אביב', 'latitude': 32.0744155, 'longitude': 34.7686057,
                'release_time': "", 'status': 'פנוי', 'hidden': False}

    parking8 = {'address': 'בן עמי 12, תל אביב', 'latitude': 32.0784095, 'longitude': 34.7729590, 'release_time': "",
                'status': 'פנוי', 'hidden': False}

    parking9 = {'address': 'המרד 36, תל אביב', 'latitude': 32.0645403, 'longitude': 34.7648474, 'release_time': "",
                'status': 'פנוי', 'hidden': False}

    parking10 = {'address': 'לילינבלום 14, תל אביב', 'latitude': 32.0619556, 'longitude': 34.7686573,
                 'release_time': "09:50", 'status': 'מתפנה בקרוב', 'hidden': False}

    parking11 = {'address': 'מחנה יוסף 34, תל אביב', 'latitude': 32.0645131, 'longitude': 34.7667812,
                 'release_time': "", 'status': 'תפוס', 'hidden': True}

    parking12 = {'address': 'דגניה 3, תל אביב', 'latitude': 32.0629708, 'longitude': 34.7647325,
                 'release_time': "", 'status': 'פנוי', 'hidden': False}

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
    starting_points = ['שדרות רוטשילד 1, תל אביב', 'בני דן 1, תל אביב', 'בן יהודה 2, תל אביב']
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
