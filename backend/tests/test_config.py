from backend.constants import MONGO_URL_ADDRESS, SECRET, FLASK_ENV_TEST, MONGO_DB_NAME

TEST = True
SECRET_KEY = SECRET  # A secret key for session encryption
# Environment Configuration
FLASK_ENV = FLASK_ENV_TEST
# MongoDB Configuration
MONGO_URI = MONGO_URL_ADDRESS
MONGO_DBNAME = MONGO_DB_NAME
