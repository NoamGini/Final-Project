from datetime import timedelta, timezone

API_HAUZOT_USERNAME = "wsu-noaziv"
API_HAUZOT_PASSWORD = "N0@z!u386"
TFAULT = "OK"
FWS_PWD = "10fd90e7004c6499fe86146fc888eee62c2d1e1ae0bf7a1c34c3346cec15fada"
GOOGLE_MAPS_API_KEY = 'AIzaSyDGG3PgHwpThGyw-BeKsaTs3mS5eS3BZXE'
GOOGLE_ENDPOINT = "https://maps.googleapis.com/maps/api/geocode/json"

SECRET_KEY = 'SECRET_KEY'
SECRET = "secret"
ENCODE_UTF8 = 'utf8'
DECODE_UTF8 = 'utf-8'

PRODUCTION_MODE = "production"
FLASK_ENV = 'FLASK_ENV'
FLASK_ENV_TEST = 'test'
DIR_TESTS = 'tests'
DIR_SRC = 'src'
MONGO_DB_NAME = "parking_spot_test"

KEY = 'key'
LANGUAGE = 'language'
HEBREW = 'he'

WSDL = 'http://parkinfo.ahuzot.co.il/cp.asmx?wsdl'

GET_ALL_DETAILS = 'GetAllCarParkStatusResult'
GET_CAR_PARK_STATIC_DETAILS = 'GetCarParkDetailsResult'
GET_CAR_PARK_DYNAMIC_DETAILS = 'CarParkDynamicDetails'
GET_CAR_PARK_STATUS_RES = 'GetCarParkStatusResult'

NAME = 'Name'
NAME2 = 'name'
ADDRESS = 'Address'
ADDRESS2 = 'address'
PARKING_AHUZOT_CODE = 'AhuzotCode'
PARKING_CENTRAL_CODE = 'CentralParkCode'
PARKING_GPS_LAT = 'GPSLattitude'
PARKING_GPS_LON = 'GPSLongitude'
INFO_TO_SHOW = 'InformationToShow'
CAPACITY = 'capacity'
FREE_PARKING_LEFT = 'free parking left'

EMAIL = 'email'
PASSWORD = 'password'
HIDDEN = 'hidden'
PARKING = 'parking'
POINTS = 'points'
RELEASE_TIME = 'release_time'
STATUS = 'status'
USER = 'user'
AVATAR = 'avatar'

STATUS_UNAVAILABLE = '    '
STATUSES = ('פנוי', 'מלא', 'מעט', 'תפוס', 'מתפנה בקרוב', '')
UPPER_BOUND = 0.15

WALKING = 'walking'
LAGS = 'legs'
DURATION = 'duration'
DISTANCE = 'distance'
VALUE = 'value'
RAW = 'raw'
TEXT = 'text'
RESULTS = 'results'
GEOMETRY = 'geometry'
LOCATION = 'location'
LATITUDE = 'lat'
LONGITUDE = 'lng'

KL_LATITUDE = 'latitude'
KL_LONGITUDE = 'longitude'

ADDRESSES_TO_CHANGE = ('שבט בנימין 1', 'כרמל 2 ', 'רידינג מערב', 'רידינג מזרח')
UPDATED_ADDRESSES = ('שבט בנימין 1 תל אביב יפו', 'סמטת הכרמל 12 תל אביב', 'רוקח 7 תל-אביב יפו', 'רוקח 15 תל-אביב יפו')
ADDRESSES_TO_DISMISS = ("פארק צ'רלס קלור", "מזאה", "White City", "רובע לב העיר", "מגדל מאייר", "דיזינגוף")
TLV = "תל-אביב יפו"
CENTRAL_PARK = "סנטרל פארק"
HAUZOT_AHOF = "אחוזת החוף"
TIMES = ('hour', 'hours', 'min', 'mins')

PARKING_LIST_URL = 'https://centralpark.co.il/רשימת-חניונים/'
STATUS_TO_FLOAT = {'פנוי': 0, '': 1}
ISRAEL_TZ = timezone(timedelta(hours=2))

EMPTY = ''
SCRIPT = 'script'
DIV = 'div'
LI = 'li'
BODY = 'body'
DECLARATIONS = 'declarations'
INIT = 'init'
CLASS_AREA_PARK_LIST = "area_parking_list"
CLASS_WRAP_PARK_DETAILS = "wrap_parking_detailes"
HTML_PARSER = "html.parser"
CLASS_INNER_LIST = "inner_list"
CLASS_AREA_HEAD = 'area_head'
ELEMENTS = 'elements'

CENTRAL_URL = f'https://centralpark.co.il/parking/'
MONGO_URL_ADDRESS = 'mongodb://localhost:27017/'
PARKING_SPOT = 'parking_spot'
CENTRAL_PARK_DB = 'central_park'
HAUZOT_AHOF_DB = 'hauzot_ahof'
PARKING_KAHOL_LAVAN_DB = 'parkings_kahol_lavan'
USERS_DB = 'users'

NONE = "None"
RESET = "reset"
EXIST = 'exist'
RESPONSE = 'response'
RESPONSE_USER_NOT_EXIST = 'User not exist'
RESPONSE_USER_ALREADY_EXIST = 'User is already exist'
RESPONSE_USER_REGISTER_SUCC = 'User registered successfully'
DATE = 'date'
RELEASE_TIME_UPDATE = 'release_time_update'
GRABBED_PARKING_UPDATE = 'grabbed_parking_update'
RELEASE_PARKING_UPDATE = 'release_parking_update'
UPDATE_PARKING_HIDDEN = 'hidden_parking_update'
UPDATE_PARKING_HIDDEN_NAME = 'Update parking hidden'

CONNECT = 'connect'
SOCKET_IO_CONNECTED = 'SocketIO client connected'
DISCONNECT = 'disconnect'
SOCKET_IO_DISCONNECTED = 'SocketIO client disconnected'

PARKING_LOTS_UPDATED = "Parking lots updated."
UPDATE_JOB = 'update_job'
UPDATE_JOB_NAME = 'Update parking lots every 5 minutes'

INVALID_ADDRESS = f'Invalid address: '
STARTING_POINTS = ['שדרות רוטשילד 1, תל אביב']
STARTING_POINTS2 = ['שדרות רוטשילד 1, תל אביב', 'בני דן 1, תל אביב', 'בן יהודה 2, תל אביב']

TEST_PARKINGS = ('Parking Lot 1', 'Parking Lot 2', 'Parking Lot 3', 'Parking Lot 4')
TEST_ADDRESSES = ('11 Main St', '12 Main St', '13 Main St', '14 Main St')
TEST_DISTANCES = (513, 1695, 1836, 1901)
TEST_DURATION = ('7 mins', '22 mins', '23 mins', '25 mins')
TEST_CODES = ('Code 1', 'Code 2', 'Code 3', 'Code 4')
TEST_STATUSES = ("free", "full", "few")

TEST_GET_PARKING_BY_NAME_EXPECTED_DATA = b'{"Name": "Parking Lot 4", "address": "14 Main St"}'
TEST_GET_PARKING_BY_NAME_RESPONSE = "Non-existent Parking Lot"