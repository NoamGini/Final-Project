from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from backend.src.mongoDB import *
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import json
from backend.constants import *


flag = 0
app = Flask(__name__)
app.config[SECRET_KEY] = SECRET
scheduler = BackgroundScheduler()
app.scheduler = scheduler

#for real time updates
socketio = SocketIO(app)

global_parking_lots_by_address = []


@app.route('/closest_parking/')
def get_all_parking_lots():
    global global_parking_lots_info

    TLV_parking_list_hauzot = get_all_data_from_collection_hauzot()
    TLV_parking_list_central = get_all_data_from_collection_central()
    all_parking_info = TLV_parking_list_hauzot + TLV_parking_list_central

    all_parking_info = json.dumps(all_parking_info, ensure_ascii=False, default=str).encode(ENCODE_UTF8)
    return all_parking_info


@app.route('/closest_parking/<address>')
def get_closest_parking_by_address_from_client(address):
    global flag, global_parking_lots_by_address

    TLV_parking_list_hauzot = get_all_data_from_collection_hauzot()
    response_hauzot = get_closest_parking_by_address_hauzot(TLV_parking_list_hauzot, address)

    TLV_parking_list_central = get_all_data_from_collection_central()
    response_central = get_closest_parking_by_address(TLV_parking_list_central, address)

    response = response_hauzot + response_central
    response = sorted(response, key=lambda x: x[1])
    ten_parking_lots = response[:10]
    global_parking_lots_by_address = ten_parking_lots
    ten_parking_lots = json.dumps(ten_parking_lots, ensure_ascii=False, default=str).encode(ENCODE_UTF8)
    flag = 0
    return ten_parking_lots


@app.route('/closest_parking/<address>/<distance>')
def get_closest_parking_by_distance_specified_by_client(address, distance):
    global global_parking_lots_by_address
    if distance == RESET:
        ten_parking_lots = json.dumps(global_parking_lots_by_address, ensure_ascii=False, default=str).encode(ENCODE_UTF8)
        return ten_parking_lots

    parking_filtered_by_distance = [tup for tup in global_parking_lots_by_address if tup[1] <= int(distance)]
    closest_parking_lot_by_distance = json.dumps(parking_filtered_by_distance, ensure_ascii=False, default=str).encode(
        ENCODE_UTF8)
    return closest_parking_lot_by_distance


@app.route('/closest_parking_duration/<address>/<duration>')
def get_closest_parking_by_duration_specified_by_client(address, duration):
    global global_parking_lots_by_address
    if duration == RESET:
        ten_parking_lots = json.dumps(global_parking_lots_by_address, ensure_ascii=False, default=str).encode(ENCODE_UTF8)
        return ten_parking_lots

    parking_filtered_by_duration = get_closest_parking_by_duration(global_parking_lots_by_address, duration)
    parking_filtered_by_duration = json.dumps(parking_filtered_by_duration, ensure_ascii=False, default=str).encode(
        ENCODE_UTF8)
    return parking_filtered_by_duration


@app.route('/closest_parking_company/<address>/<company>')
def get_parking_by_company(address, company):
    global flag, global_parking_lots_by_address
    response = []
    if company == RESET:
        ten_parking_lots = json.dumps(global_parking_lots_by_address, ensure_ascii=False, default=str).encode(ENCODE_UTF8)
        return ten_parking_lots
    if company == HAUZOT_AHOF:
        flag = 1
        for parking in global_parking_lots_by_address:
            if PARKING_AHUZOT_CODE in parking[0]:
                response.append(parking)
    if company == CENTRAL_PARK:
        flag = 2
        for parking in global_parking_lots_by_address:
            if PARKING_CENTRAL_CODE in parking[0]:
                response.append(parking)

    response = json.dumps(response, ensure_ascii=False, default=str).encode(ENCODE_UTF8)
    return response


@app.route('/closest_parking_status/<address>/<status>')
def get_parking_by_status(address, status):
    global global_parking_lots_by_address
    if status == RESET:
        ten_parking_lots = json.dumps(global_parking_lots_by_address, ensure_ascii=False, default=str).encode(ENCODE_UTF8)
        return ten_parking_lots

    parking_lots_by_status = [tup for tup in global_parking_lots_by_address if tup[0]['InformationToShow'] == status]
    parking_lots_by_status = json.dumps(parking_lots_by_status, ensure_ascii=False, default=str).encode(
        ENCODE_UTF8)
    return parking_lots_by_status


@app.route('/closest_parking_by_parking_name/<parking_name>')
def get_parking_by_name(parking_name):
    TLV_parking_list_hauzot = get_all_data_from_collection_hauzot()
    TLV_parking_list_central = get_all_data_from_collection_central()
    all_parking_lots = TLV_parking_list_hauzot + TLV_parking_list_central

    for park in all_parking_lots:
        if park[NAME] == parking_name:
            park = json.dumps(park, ensure_ascii=False, default=str).encode(ENCODE_UTF8)
            return park
    return NONE


@app.route('/register', methods=['POST'])
def register():
    request_data = request.data  # getting the response data
    request_data = json.loads(request_data.decode(DECODE_UTF8))
    email = request_data[EMAIL]
    name = request_data[NAME2]
    password = request_data[PASSWORD]
    parking = request_data[PARKING]
    points = request_data[POINTS]
    avatar = request_data[AVATAR]
    user = {NAME2: name, EMAIL: email, PASSWORD: password, PARKING: parking, POINTS: points, AVATAR: avatar }
    # check if this user already exits
    if not user_exist_db(user):
        add_user_to_db(user)
        response = RESPONSE_USER_REGISTER_SUCC
        return jsonify({RESPONSE: response})
    response = RESPONSE_USER_ALREADY_EXIST
    return jsonify({RESPONSE: response})


@app.route('/signIn', methods=['POST'])
def signIn():
    request_data = request.data  # getting the response data
    request_data = json.loads(request_data.decode(DECODE_UTF8))
    email = request_data[EMAIL]
    password = request_data[PASSWORD]
    if user_exist_by_email_password(email, password):
        response = EXIST
        return jsonify({RESPONSE: response})
    response = RESPONSE_USER_NOT_EXIST
    return jsonify({RESPONSE: response})


@app.route('/signInGet', methods=['POST'])
def get_user():
    request_data = request.data  # getting the response data
    request_data = json.loads(request_data.decode(DECODE_UTF8))
    email = request_data[EMAIL]
    password = request_data[PASSWORD]
    user = get_user_by_email_password(email, password)
    user = json.dumps(user, ensure_ascii=False, default=str).encode(ENCODE_UTF8)
    return user


@app.route('/parking_kahol_lavan')
def get_all_parking_kahol_lavan():
    all_parking_kahol_lavan= get_all_data_from_collection_kahol_lavan()
    all_parking_kahol_lavan = json.dumps(all_parking_kahol_lavan, ensure_ascii=False, default=str).encode(ENCODE_UTF8)
    return all_parking_kahol_lavan

@app.route('/parking_kahol_lavan/release_time', methods=['POST'])
def update_release_time():
    request_data = request.data  # getting the response data
    request_data = json.loads(request_data.decode(DECODE_UTF8))
    email = request_data[EMAIL]
    address = request_data[ADDRESS2]
    release_time = request_data[RELEASE_TIME]
    user, parking= update_parking_release_time(email, address, release_time)
    parking = json.dumps(parking, ensure_ascii=False, default=str).encode(ENCODE_UTF8)
    user = json.dumps(user, ensure_ascii=False, default=str).encode(ENCODE_UTF8)
    # Update the data
    socketio.emit(RELEASE_TIME_UPDATE, parking)

    return user


@app.route('/parking_kahol_lavan/grabbing_parking', methods=['POST'])
def update_grabbed_parking():
    request_data = request.data  # getting the response data
    request_data = json.loads(request_data.decode(DECODE_UTF8))
    email = request_data[EMAIL]
    address = request_data[ADDRESS2]
    user, parking = update_grabbing_parking(email, address)
    user = json.dumps(user, ensure_ascii=False, default=str).encode(ENCODE_UTF8)
    parking = json.dumps(parking, ensure_ascii=False, default=str).encode(ENCODE_UTF8)
    # Update the data
    socketio.emit(GRABBED_PARKING_UPDATE, parking)

    # Schedule the parking status update after 30 seconds
    scheduler.add_job(
        func=update_parking_hidden,
        trigger=DATE,
        run_date=datetime.now() + timedelta(seconds=30),
        args=(email, address),  # Pass the parking address as an argument
        id=UPDATE_PARKING_HIDDEN,
        name=UPDATE_PARKING_HIDDEN_NAME
    )
    return user


@app.route('/parking_kahol_lavan/points', methods=['POST'])
def get_points():
    request_data = request.data  # getting the response data
    request_data = json.loads(request_data.decode(DECODE_UTF8))
    user = request_data[USER]
    points = get_user_points(user)
    points = json.dumps(points, ensure_ascii=False, default=str).encode(ENCODE_UTF8)
    return points


@app.route('/parking_kahol_lavan/release_parking', methods=['POST'])
def update_release_parking():
    request_data = request.data  # getting the response data
    request_data = json.loads(request_data.decode(DECODE_UTF8))
    email = request_data[EMAIL]
    address = request_data[ADDRESS2]
    user, parking = update_parking_release(email, address)
    parking = json.dumps(parking, ensure_ascii=False, default=str).encode(ENCODE_UTF8)
    user = json.dumps(user, ensure_ascii=False, default=str).encode(ENCODE_UTF8)
    # Update the data
    socketio.emit(RELEASE_PARKING_UPDATE, parking)
    return user

# Define Socket.IO event handlers
@socketio.on(CONNECT)
def handle_connect():
    print(SOCKET_IO_CONNECTED)

@socketio.on(DISCONNECT)
def handle_disconnect():
    print(SOCKET_IO_DISCONNECTED)

def update_parking_hidden(email, address):
    parking = update_parking_status_hidden(email, address)
    parking = json.dumps(parking, ensure_ascii=False, default=str).encode(ENCODE_UTF8)
    # Update the data
    socketio.emit(UPDATE_PARKING_HIDDEN, parking)


def update_parking_lots():

    # Get the data from the database
    TLV_parking_list_hauzot = get_all_data_from_collection_hauzot()
    TLV_parking_list_central = get_all_data_from_collection_central()

    # Perform the update for each parking lot
    for parking in TLV_parking_list_hauzot:
        updated_parking_hauzot = update_status(parking, parking[PARKING_AHUZOT_CODE])
        parking[INFO_TO_SHOW] = updated_parking_hauzot[INFO_TO_SHOW]
        filter_query = {NAME: parking[NAME]}
        update_query = {'$set': {INFO_TO_SHOW: updated_parking_hauzot[INFO_TO_SHOW]}}
        update_document(HAUZOT_AHOF_DB, filter_query, update_query)

    for parking in TLV_parking_list_central:
        parking_tuple = (parking, EMPTY)
        updated_parking_central = update_parking_lot_status(parking_tuple)
        parking[INFO_TO_SHOW] = updated_parking_central[0][INFO_TO_SHOW]
        filter_query = {NAME: updated_parking_central[0][NAME]}
        update_query = {'$set': {INFO_TO_SHOW: updated_parking_central[0][INFO_TO_SHOW]}}
        update_document(CENTRAL_PARK_DB, filter_query, update_query)

    print(PARKING_LOTS_UPDATED)



# Configure the scheduler
scheduler.add_job(
    func=update_parking_lots,
    trigger=IntervalTrigger(minutes=5),
    id=UPDATE_JOB,
    name=UPDATE_JOB_NAME,
    replace_existing=True
)


if __name__ == "__main__":
    scheduler.start()
    socketio.run(app, allow_unsafe_werkzeug=True)
