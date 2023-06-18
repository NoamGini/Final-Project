import os
from backend.src import create_app
from backend.src.server import socketio

if __name__ == "__main__":
    # For the test environment:
    os.environ['FLASK_ENV'] = 'test'
    app, db = create_app(config_filename='test_config.py')
    socketio.run(app, allow_unsafe_werkzeug=True)
