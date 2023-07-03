import pymongo
from backend.src.getDataFromURL import *
from backend.src.getDataFromAPI import *
from backend.src.users import *
from backend.src.parking_kahol_lavan import *
from pymongo import MongoClient
from backend.constants import *


def update_document(collection_name, filter_query, update_query):
    client = MongoClient()  # Connect to default MongoDB server running on localhost
    db = client.mydatabase  # Select the database to work with
    collection = db[collection_name]  # Select the collection to update document

    result = collection.update_one(filter_query, update_query)


def insert_parking_lot_data_to_mongodb():
    # Set up MongoDB client and connect to database
    client = pymongo.MongoClient(MONGO_URL_ADDRESS)
    db = client[PARKING_SPOT]

    collection1 = db[CENTRAL_PARK_DB]
    data1 = get_parking_list()
    for parking in data1:
        collection1.insert_one(parking)

    collection2 = db[HAUZOT_AHOF_DB]
    data2 = get_all_parking_lots_info_hauzot()
    for parking in data2:
        collection2.insert_one(parking)
    # Close MongoDB client
    client.close()


def insert_users_data_to_mongodb():
    # Set up MongoDB client and connect to database
    client = pymongo.MongoClient(MONGO_URL_ADDRESS)
    db = client[PARKING_SPOT]

    collection1 = db[USERS_DB]
    users_data = create_users_list()
    for user in users_data:
        collection1.insert_one(user)
    # Close MongoDB client
    client.close()


def insert_parking_kahol_lavan_data_to_mongodb():
    # Set up MongoDB client and connect to database
    client = pymongo.MongoClient(MONGO_URL_ADDRESS)
    db = client[PARKING_SPOT]

    collection1 = db[PARKING_KAHOL_LAVAN_DB]
    parking_data = generate_list_kahol_lavan()
    for parking in parking_data:
        collection1.insert_one(parking)
    # Close MongoDB client
    client.close()


def get_all_data_from_collection_central():
    # Set up MongoDB client and connect to database
    client_central = pymongo.MongoClient(MONGO_URL_ADDRESS)
    db = client_central[PARKING_SPOT]

    # Get all data from MongoDB collection
    collection = db[CENTRAL_PARK_DB]
    data = collection.find()
    list_data = list(data)

    # Close MongoDB client
    client_central.close()

    # Return data as a list
    return list_data


def get_all_data_from_collection_hauzot():
    # Set up MongoDB client and connect to database
    client_hauzot = pymongo.MongoClient(MONGO_URL_ADDRESS)
    db = client_hauzot[PARKING_SPOT]

    # Get all data from MongoDB collection
    collection = db[HAUZOT_AHOF_DB]
    data = collection.find()
    list_data = list(data)

    # Close MongoDB client
    client_hauzot.close()

    # Return data as a list
    return list_data


def add_user_to_db(user):
    client = MongoClient(MONGO_URL_ADDRESS)  # replace with your MongoDB URI
    db = client[PARKING_SPOT]  # replace with your database name
    collection = db[USERS_DB]  # replace with your collection name
    collection.insert_one(user)
    # Close MongoDB client
    client.close()


def get_all_data_from_collection_kahol_lavan():
    # Set up MongoDB client and connect to database
    client_hauzot = pymongo.MongoClient(MONGO_URL_ADDRESS)
    db = client_hauzot[PARKING_SPOT]

    # Get all data from MongoDB collection
    collection = db[PARKING_KAHOL_LAVAN_DB]
    data = collection.find()
    list_data = list(data)

    # Close MongoDB client
    client_hauzot.close()

    # Return data as a list
    return list_data


def update_parking_release_time(email, address, release_time):
    client = MongoClient(MONGO_URL_ADDRESS)  # replace with your MongoDB URI
    db = client[PARKING_SPOT]  # replace with your database name
    collection = db[PARKING_KAHOL_LAVAN_DB]  # replace with your collection name
    resultParking = collection.find({ADDRESS_SMALL_LETTER: address})
    parkingDB = None
    userDB = None
    for i in resultParking:
        parkingDB = i
        collection.update_one({ADDRESS_SMALL_LETTER: parkingDB[ADDRESS_SMALL_LETTER]},
                              {'$set': {RELEASE_TIME: release_time,
                                        STATUS: STATUSES[4], HIDDEN: False}})
        parkingDB[RELEASE_TIME] = release_time
        parkingDB[STATUS] = STATUSES[4]
        break

    collection2 = db[USERS_DB]
    resultUser = collection2.find({EMAIL: email})
    for i in resultUser:
        userDB = i
        points = userDB[POINTS]
        points += 1
        collection2.update_one({EMAIL: userDB[EMAIL]}, {'$set': {POINTS: points, PARKING: parkingDB}})
        userDB[PARKING] = parkingDB
        break
    # Close MongoDB client
    client.close()
    return userDB, parkingDB


def update_parking_release(email, address):
    client = MongoClient(MONGO_URL_ADDRESS)  # replace with your MongoDB URI
    db = client[PARKING_SPOT]  # replace with your database name
    collection1 = db[USERS_DB]  # replace with your collection name
    # add points to the user

    # Initialize userDB with None
    userDB = None

    resultUser = collection1.find({EMAIL: email})
    for i in resultUser:
        userDB = i
        points = userDB[POINTS]
        points += 2
        userDB[POINTS] = points
        userDB[PARKING] = None
        collection1.update_one({EMAIL: email}, {'$set': {PARKING: None, POINTS: points}})
        break

    collection2 = db[PARKING_KAHOL_LAVAN_DB]  # replace with your collection name
    resultParking = collection2.find({ADDRESS_SMALL_LETTER: address})
    parkingDB = None
    for i in resultParking:
        parkingDB = i
        collection2.update_one({ADDRESS_SMALL_LETTER: parkingDB[ADDRESS_SMALL_LETTER]},
                               {'$set': {RELEASE_TIME: EMPTY, STATUS: STATUSES[0],
                                         HIDDEN: False, }})
        parkingDB[STATUS] = STATUSES[0]
        parkingDB[RELEASE_TIME] = EMPTY
        parkingDB[HIDDEN] = False
        break

    # Close MongoDB client
    client.close()
    return userDB, parkingDB


def update_grabbing_parking(email, address):
    client = MongoClient(MONGO_URL_ADDRESS)  # replace with your MongoDB URI
    db = client[PARKING_SPOT]  # replace with your database name
    users_collection = db[USERS_DB]  # replace with your collection name

    # Check if there is a user with the given parking and release the parking
    users_with_parking = users_collection.count_documents({PARKING: address})
    if users_with_parking > 0:
        users_to_update = users_collection.find({PARKING: address})
        for user in users_to_update:
            users_collection.update_one({EMAIL: user[EMAIL]}, {'$set': {PARKING: None}})

    # add points to the user
    userDB = None
    resultUser = users_collection.find({EMAIL: email})
    for i in resultUser:
        userDB = i
        points = userDB[POINTS]
        points += 2
        userDB[POINTS] = points
        users_collection.update_one({EMAIL: email}, {'$set': {POINTS: points}})
        break

    parking_collection = db[PARKING_KAHOL_LAVAN_DB]  # replace with your collection name
    resultParking = parking_collection.find({ADDRESS_SMALL_LETTER: address})
    parkingDB = None
    for i in resultParking:
        parkingDB = i
        parking_collection.update_one({ADDRESS_SMALL_LETTER: parkingDB[ADDRESS_SMALL_LETTER]},
                                      {'$set': {RELEASE_TIME: EMPTY, STATUS: STATUSES[3], }})
        parkingDB[STATUS] = STATUSES[3]
        parkingDB[RELEASE_TIME] = EMPTY
        parking_collection.update_one({EMAIL: email}, {'$set': {PARKING: parkingDB}})
        userDB[PARKING] = parkingDB
        break

    # Close MongoDB client
    client.close()
    return userDB, parkingDB


def get_user_points(user):
    client = MongoClient(MONGO_URL_ADDRESS)  # replace with your MongoDB URI
    db = client[PARKING_SPOT]  # replace with your database name
    collection = db[USERS_DB]
    result = collection.find({NAME_SMALL_LETTER: user[NAME_SMALL_LETTER], EMAIL: user[EMAIL]})
    for i in result:
        user = i
    points = user[POINTS]
    return points


def update_parking_status_hidden(email, address):
    client = MongoClient(MONGO_URL_ADDRESS)
    db = client[PARKING_SPOT]
    parking_collection = db[PARKING_KAHOL_LAVAN_DB]
    users_collection = db[USERS_DB]
    resultParking = parking_collection.find({ADDRESS_SMALL_LETTER: address})
    parkingDB = None
    for i in resultParking:
        parkingDB = i
        # parkingDB = parking_collection.find_one_and_update(
        #     {'address': parkingDB['address']}, {'$set': {'hidden': True, }})
        parking_collection.update_one({ADDRESS_SMALL_LETTER: parkingDB[ADDRESS_SMALL_LETTER]},
                                      {'$set': {HIDDEN: True, }})
        parkingDB[HIDDEN] = True
        break

    # add points to the user
    userDB = None
    resultUser = users_collection.find({EMAIL: email})
    for i in resultUser:
        userDB = i
        # userDB = users_collection.parking_collection.find_one_and_update({'email': userDB['email']},
        #                                                                  {'$set': {'parking': parkingDB}})
        users_collection.update_one({EMAIL: userDB[EMAIL]}, {'$set': {PARKING: parkingDB}})
        parkingDB[HIDDEN] = True
        break

    # Close MongoDB client
    client.close()
    return parkingDB


def user_exist_db(user):
    client = MongoClient(MONGO_URL_ADDRESS)  # replace with your MongoDB URI
    db = client[PARKING_SPOT]  # replace with your database name
    collection = db[USERS_DB]
    result = collection.find({NAME_SMALL_LETTER: user[NAME_SMALL_LETTER], EMAIL: user[EMAIL]})
    for i in result:
        if i is not None:
            client.close()
            return True
    client.close()
    return False


def user_exist_by_email_password(email, password):
    client = MongoClient(MONGO_URL_ADDRESS)  # replace with your MongoDB URI
    db = client[PARKING_SPOT]  # replace with your database name
    collection = db[USERS_DB]
    result = collection.find({EMAIL: email, PASSWORD: password})
    for i in result:
        if i is not None:
            client.close()
            return True
    client.close()
    return False


def get_user_by_email_password(email, password):
    client = MongoClient(MONGO_URL_ADDRESS)  # replace with your MongoDB URI
    db = client[PARKING_SPOT]  # replace with your database name
    collection = db[USERS_DB]
    result = collection.find({EMAIL: email, PASSWORD: password})
    user = None
    for i in result:
        user = i
        client.close()
        return user
    client.close()
    return user


def get_parking_kl_by_address(address):
    client = MongoClient(MONGO_URL_ADDRESS)  # replace with your MongoDB URI
    db = client[PARKING_SPOT]  # replace with your database name
    collection = db[PARKING_KAHOL_LAVAN_DB]
    result = collection.find({ADDRESS_SMALL_LETTER: address})
    parking = None
    for i in result:
        parking = i
        client.close()
        return parking
    client.close()
    return parking


def update_park_lot_status(updated_status, parking_name, db_name):
    filter_query = {NAME: parking_name}
    update_query = {'$set': {INFO_TO_SHOW: updated_status}}
    update_document(db_name, filter_query, update_query)


def main():
    # insert_parking_kahol_lavan_data_to_mongodb()
    insert_users_data_to_mongodb()
    # users_list = get_users_list()
    # get_user_points(users_list[0])
    # kahol_lavan_list= get_parking_kahol_lavan_list()
    # update_parking_release(users_list[0]['email'],kahol_lavan_list[0]['address'])
    # users_list = get_users_list()
    # kahol_lavan_list= get_parking_kahol_lavan_list()
    # update_grabbing_parking(users_list[0]['email'], kahol_lavan_list[0]['address'])
    # update_parking_release_time(users_list[0]['email'],kahol_lavan_list[0]['address'],'14:40')
    # insert_parking_lot_data_to_mongodb()
    # result = get_user_by_email_password("avi@gmail.com","12345678")
    # print(result)


if __name__ == "__main__":
    # response = get_parking_lot_location(43)
    # print(response)
    main()
