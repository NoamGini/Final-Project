from backend.src import create_app
from backend.src.server import socketio

if __name__ == "__main__":
    db_uri = "mongodb://127.0.0.1:27017/"
    db_name = 'parking_spot'
    app, db = create_app(config_filename='config.py')  # Specify the test configuration file
    socketio.run(app, allow_unsafe_werkzeug=True)
