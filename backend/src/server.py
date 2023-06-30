from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from backend.src.mongoDB import *
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger


flag = 0
app = Flask(__name__)
#app.config["DEBUG"]=True
app.config["SECRET_KEY"] = "secret"
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

    all_parking_info = json.dumps(all_parking_info, ensure_ascii=False, default=str).encode('utf8')
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
    ten_parking_lots = json.dumps(ten_parking_lots, ensure_ascii=False, default=str).encode('utf8')
    flag = 0
    return ten_parking_lots


@app.route('/closest_parking/<address>/<distance>', endpoint='func2')
def get_closest_parking_by_distance_specified_by_client(address, distance):
    global global_parking_lots_by_address
    if distance == "reset":
        ten_parking_lots = json.dumps(global_parking_lots_by_address, ensure_ascii=False, default=str).encode('utf8')
        return ten_parking_lots

    parking_filtered_by_distance = [tup for tup in global_parking_lots_by_address if tup[1] <= int(distance)]
    closest_parking_lot_by_distance = json.dumps(parking_filtered_by_distance, ensure_ascii=False, default=str).encode(
        'utf8')
    return closest_parking_lot_by_distance


@app.route('/closest_parking_duration/<address>/<duration>')
def get_closest_parking_by_duration_specified_by_client(address, duration):
    global global_parking_lots_by_address
    if duration == "reset":
        ten_parking_lots = json.dumps(global_parking_lots_by_address, ensure_ascii=False, default=str).encode('utf8')
        return ten_parking_lots

    parking_filtered_by_duration = get_closest_parking_by_duration(global_parking_lots_by_address, duration)
    parking_filtered_by_duration = json.dumps(parking_filtered_by_duration, ensure_ascii=False, default=str).encode(
        'utf8')
    return parking_filtered_by_duration


@app.route('/closest_parking_company/<address>/<company>', endpoint='func1')
def get_parking_by_company(address, company):
    global flag, global_parking_lots_by_address
    response = []
    if company == "reset":
        ten_parking_lots = json.dumps(global_parking_lots_by_address, ensure_ascii=False, default=str).encode('utf8')
        return ten_parking_lots
    if company == "אחוזת החוף":
        flag = 1
        for parking in global_parking_lots_by_address:
            if "AhuzotCode" in parking[0]:
                response.append(parking)
    if company == "סנטרל פארק":
        flag = 2
        for parking in global_parking_lots_by_address:
            if "CentralParkCode" in parking[0]:
                response.append(parking)

    response = json.dumps(response, ensure_ascii=False, default=str).encode('utf8')
    return response


@app.route('/closest_parking_status/<address>/<status>')
def get_parking_by_status(address, status):
    global global_parking_lots_by_address
    if status == "reset":
        ten_parking_lots = json.dumps(global_parking_lots_by_address, ensure_ascii=False, default=str).encode('utf8')
        return ten_parking_lots

    parking_lots_by_status = [tup for tup in global_parking_lots_by_address if tup[0]['InformationToShow'] == status]
    parking_lots_by_status = json.dumps(parking_lots_by_status, ensure_ascii=False, default=str).encode(
        'utf8')
    return parking_lots_by_status


@app.route('/closest_parking_by_parking_name/<parking_name>')
def get_parking_by_name(parking_name):
    TLV_parking_list_hauzot = get_all_data_from_collection_hauzot()
    TLV_parking_list_central = get_all_data_from_collection_central()
    all_parking_lots = TLV_parking_list_hauzot + TLV_parking_list_central

    for park in all_parking_lots:
        if park['Name'] == parking_name:
            park = json.dumps(park, ensure_ascii=False, default=str).encode('utf8')
            return park
    return "None"


@app.route('/register', methods=['POST'])
def register():
    request_data = request.data  # getting the response data
    request_data = json.loads(request_data.decode('utf-8'))
    print('hi')
    email = request_data['email']
    name = request_data['name']
    password = request_data['password']
    parking = request_data['parking']
    points = request_data['points']
    avatar = request_data['avatar']
    user = {'name': name, 'email': email, 'password': password, 'parking': parking, 'points': points, 'avatar': avatar }
    # check if this user already exits
    if not user_exist_db(user):
        add_user_to_db(user)
        print('added')
        response = 'User registered successfully'
        return jsonify({'response': response})
    print("user exists")
    response = 'User is already exist'
    return jsonify({'response': response})


@app.route('/signIn', methods=['POST'])
def signIn():
    request_data = request.data  # getting the response data
    request_data = json.loads(request_data.decode('utf-8'))
    print('hi')
    email = request_data['email']
    password = request_data['password']
    print(email)
    print(password)
    if user_exist_by_email_password(email, password):
        #add_user_to_db(user)
        #print('added')
        response = 'exist'
        return jsonify({'response': response})
    print("user not exists")
    response = 'User not exist'
    return jsonify({'response': response})


@app.route('/signInGet', methods=['POST'])
def get_user():
    request_data = request.data  # getting the response data
    request_data = json.loads(request_data.decode('utf-8'))
    print(request_data)
    print('hi')
    email = request_data['email']
    password = request_data['password']
    print(email)
    print(password)
    user = get_user_by_email_password(email, password)
    print(user)
    user = json.dumps(user, ensure_ascii=False, default=str).encode('utf8')
    print(user)
    return user


@app.route('/parking_kahol_lavan')
def get_all_parking_kahol_lavan():
    all_parking_kahol_lavan= get_all_data_from_collection_kahol_lavan()
    print(all_parking_kahol_lavan)
    all_parking_kahol_lavan = json.dumps(all_parking_kahol_lavan, ensure_ascii=False, default=str).encode('utf8')
    return all_parking_kahol_lavan

@app.route('/parking_kahol_lavan/release_time', methods=['POST'])
def update_release_time():
    request_data = request.data  # getting the response data
    request_data = json.loads(request_data.decode('utf-8'))
    print(request_data)
    # user = request_data['user']
    # parking = request_data['parking']
    email = request_data['email']
    address = request_data['address']
    release_time = request_data['release_time']
    user, parking= update_parking_release_time(email, address, release_time)
    print(user)
    parking = json.dumps(parking, ensure_ascii=False, default=str).encode('utf8')
    print(parking)
    user = json.dumps(user, ensure_ascii=False, default=str).encode('utf8')
    print(user)
    # Update the data
    socketio.emit('release_time_update', parking)

    return user


@app.route('/parking_kahol_lavan/grabbing_parking', methods=['POST'])
def update_grabbed_parking():
    request_data = request.data  # getting the response data
    request_data = json.loads(request_data.decode('utf-8'))
    print(request_data)
    email = request_data['email']
    address = request_data['address']
    user, parking = update_grabbing_parking(email, address)
    print(user)
    user = json.dumps(user, ensure_ascii=False, default=str).encode('utf8')
    print(user)
    parking = json.dumps(parking, ensure_ascii=False, default=str).encode('utf8')
    print(parking)
    # Update the data
    socketio.emit('grabbed_parking_update', parking)
    return user


@app.route('/parking_kahol_lavan/points', methods=['POST'])
def get_points():
    request_data = request.data  # getting the response data
    request_data = json.loads(request_data.decode('utf-8'))
    print(request_data)
    user = request_data['user']
    points = get_user_points(user)
    print(points)
    points = json.dumps(points, ensure_ascii=False, default=str).encode('utf8')
    return points


@app.route('/parking_kahol_lavan/release_parking', methods=['POST'])
def update_release_parking():
    request_data = request.data  # getting the response data
    request_data = json.loads(request_data.decode('utf-8'))
    print(request_data)
    # user = request_data['user']
    # park = request_data['park']
    email = request_data['email']
    address = request_data['address']
    #old_parking = get_parking_kl_by_address(address)
    #print(old_parking)
    user, parking = update_parking_release(email, address)
    parking = json.dumps(parking, ensure_ascii=False, default=str).encode('utf8')
    print(parking)
    user = json.dumps(user, ensure_ascii=False, default=str).encode('utf8')
    print(user)
    # Update the data
    socketio.emit('release_parking_update', parking)
    return user

# Define Socket.IO event handlers
@socketio.on('connect')
def handle_connect():
    print('SocketIO client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('SocketIO client disconnected')

def update_parking_lots():
    #global global_parking_lots_by_address

    # Get the data from the database
    TLV_parking_list_hauzot = get_all_data_from_collection_hauzot()
    TLV_parking_list_central = get_all_data_from_collection_central()

    # Perform the update for each parking lot
    for parking in TLV_parking_list_hauzot:
        updated_parking_hauzot = update_status(parking, parking['AhuzotCode'])
        parking['InformationToShow'] = updated_parking_hauzot['InformationToShow']
        filter_query = {'Name': parking['Name']}
        update_query = {'$set': {'InformationToShow': updated_parking_hauzot['InformationToShow']}}
        update_document("hauzot_ahof", filter_query, update_query)

    for parking in TLV_parking_list_central:
        parking_tuple = (parking, "")
        updated_parking_central = update_parking_lot_status(parking_tuple)
        parking['InformationToShow'] = updated_parking_central[0]['InformationToShow']
        filter_query = {'Name': updated_parking_central[0]['Name']}
        update_query = {'$set': {'InformationToShow': updated_parking_central[0]['InformationToShow']}}
        update_document("central_park", filter_query, update_query)

    print("Parking lots updated.")
    #
    # # Update the global_parking_lots_by_address variable
    # TLV_parking_list = TLV_parking_list_hauzot + TLV_parking_list_central
    # response = get_closest_parking_by_address_hauzot(TLV_parking_list, address) + get_closest_parking_by_address(TLV_parking_list_central, address)
    # response = sorted(response, key=lambda x: x[1])
    # global_parking_lots_by_address = response[:10]


# Configure the scheduler
scheduler.add_job(
    func=update_parking_lots,
    trigger=IntervalTrigger(minutes=5),
    id='update_job',
    name='Update parking lots every 5 minutes',
    replace_existing=True
)


if __name__ == "__main__":
    # response = get_parking_lot_location(43)
    # print(response)
    # app.run()
    #allow_unsafe_werkzeug = True
    # Start the scheduler
    #get_closest_parking_by_address_from_client("המרד 30, תל אביב")
    scheduler.start()
    socketio.run(app, allow_unsafe_werkzeug=True)
