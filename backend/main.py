from backend.src import create_app
from backend.src.server import socketio
from backend.constants import MONGO_URL_ADDRESS, PARKING_SPOT

if __name__ == "__main__":
    db_uri = MONGO_URL_ADDRESS
    db_name = PARKING_SPOT
    app, db = create_app(config_filename='config.py')  # Specify the test configuration file
    socketio.run(app, allow_unsafe_werkzeug=True)
