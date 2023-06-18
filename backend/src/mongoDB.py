import pymongo
from getDataFromURL import *
from getDataFromAPI import *
from users import *
from parking_kahol_lavan import *
from pymongo import MongoClient


def update_document(collection_name, filter_query, update_query):
    """
    Update a document in the specified MongoDB collection.
    :param collection_name: Name of the collection to update document.
    :param filter_query: Filter query to select the document to update.
    :param update_query: Update query to apply on the selected document.
    :return: None
    """
    client = MongoClient()  # Connect to default MongoDB server running on localhost
    db = client.mydatabase  # Select the database to work with
    collection = db[collection_name]  # Select the collection to update document

    result = collection.update_one(filter_query, update_query)

def insert_parking_lot_data_to_mongodb():
    # Set up MongoDB client and connect to database
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['parking_spot']

    collection1 = db['central_park']
    data1 = get_parking_list()
    for parking in data1:
        collection1.insert_one(parking)

    collection2 = db['hauzot_ahof']
    data2 = get_all_parking_lots_info_hauzot()
    for parking in data2:
        collection2.insert_one(parking)
    # Close MongoDB client
    client.close()

def insert_users_data_to_mongodb():
    # Set up MongoDB client and connect to database
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['parking_spot']

    collection1 = db['users']
    users_data = get_users_list()
    for user in users_data:
        collection1.insert_one(user)
    # Close MongoDB client
    client.close()

def insert_parking_kahol_lavan_data_to_mongodb():
    # Set up MongoDB client and connect to database
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['parking_spot']

    collection1 = db['parkings_kahol_lavan']
    parking_data = get_parking_kahol_lavan_list()
    for parking in parking_data:
        collection1.insert_one(parking)
    # Close MongoDB client
    client.close()

def get_all_data_from_collection_central():
    # Set up MongoDB client and connect to database
    client_central = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client_central['parking_spot']

    # Get all data from MongoDB collection
    collection = db['central_park']
    data = collection.find()
    list_data = list(data)

    # Close MongoDB client
    client_central.close()

    # Return data as a list
    return list_data


def get_all_data_from_collection_hauzot():
    # Set up MongoDB client and connect to database
    client_hauzot = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client_hauzot['parking_spot']

    # Get all data from MongoDB collection
    collection = db['hauzot_ahof']
    data = collection.find()
    list_data = list(data)

    # Close MongoDB client
    client_hauzot.close()

    # Return data as a list
    return list_data


def add_user_to_db(user):
    client = MongoClient('mongodb://localhost:27017/')  # replace with your MongoDB URI
    db = client['parking_spot']  # replace with your database name
    collection = db['users']  # replace with your collection name
    collection.insert_one(user)
    # Close MongoDB client
    client.close()


# def add_parking_to_db(user):
#     client = MongoClient('mongodb://localhost:27017/')  # replace with your MongoDB URI
#     db = client['parking_spot']  # replace with your database name
#     collection = db['users']  # replace with your collection name
#     collection.insert_one(user)
#     # Close MongoDB client
#     client.close()


def get_all_data_from_collection_kahol_lavan():
    # Set up MongoDB client and connect to database
    client_hauzot = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client_hauzot['parking_spot']

    # Get all data from MongoDB collection
    collection = db['parkings_kahol_lavan']
    data = collection.find()
    list_data = list(data)

    # Close MongoDB client
    client_hauzot.close()

    # Return data as a list
    return list_data


def update_parking_release_time(email, address, release_time):
    client = MongoClient('mongodb://localhost:27017/')  # replace with your MongoDB URI
    db = client['parking_spot']  # replace with your database name
    collection = db['parkings_kahol_lavan']  # replace with your collection name
    resultParking = collection.find({'address': address})
    parkingDB = None
    userDB = None
    for i in resultParking:
        print(i)
        parkingDB = i
        collection.update_one({'address': parkingDB['address']}, {'$set': {'release_time': release_time,
                                                                     'status': 'מתפנה בקרוב'}})
        parkingDB['release_time'] = release_time
        parkingDB['status'] = 'מתפנה בקרוב'
        break

    collection2 = db['users']
    resultUser = collection2.find({'email': email})
    for i in resultUser:
        print(i)
        userDB = i
        points = userDB['points']
        points += 1
        collection2.update_one({'email': userDB['email']}, {'$set': {'points': points, 'parking': parkingDB}})
        userDB['parking'] = parkingDB
        break
    # Close MongoDB client
    client.close()
    print(userDB)
    return userDB, parkingDB




# def update_parking_release(user, parking):
#     client = MongoClient('mongodb://localhost:27017/')  # replace with your MongoDB URI
#     db = client['parking_spot']  # replace with your database name
#     collection1 = db['users']  # replace with your collection name
#     #add points to the user
#     resultUser = collection1.find({'name': user['name'], 'email': user['email']})
#     for i in resultUser:
#         print(i)
#         userDB = i
#     points = userDB['points']
#     points += 2
#     collection1.update_one({'email': userDB['email']}, {'$set': {'parking': None, 'points': points}})
#
#     collection2 = db['parkings_kahol_lavan']  # replace with your collection name
#     resultParking = collection1.find({'address': parking['address']})
#     parkingDB = parking
#     for i in resultParking:
#         print(i)
#         parkingDB = i
#
#     collection2.update_one({'address': parkingDB['address']}, {'$set': {'release_time': "", 'status': 'פנוי'}})
#
#     client.close()


def update_parking_release(email, address):
    client = MongoClient('mongodb://localhost:27017/')  # replace with your MongoDB URI
    db = client['parking_spot']  # replace with your database name
    collection1 = db['users']  # replace with your collection name
    # add points to the user

    # Initialize userDB with None
    userDB = None

    resultUser = collection1.find({'email': email})
    for i in resultUser:
        print(i)
        userDB = i
        points = userDB['points']
        points += 2
        userDB['points'] = points
        userDB['parking'] = None
        collection1.update_one({'email': email}, {'$set': {'parking': None, 'points': points}})
        break

    collection2 = db['parkings_kahol_lavan']  # replace with your collection name
    resultParking = collection2.find({'address': address})
    parkingDB = None
    print(resultParking)
    for i in resultParking:
        print(i)
        parkingDB = i
        collection2.update_one({'address': parkingDB['address']}, {'$set': {'release_time': "", 'status': 'פנוי', }})
        parkingDB['status']='פנוי'
        parkingDB['release_time']=""
        break

    # Close MongoDB client
    client.close()
    print("printing userDB")
    print(userDB)
    return userDB, parkingDB


def update_grabbing_parking(email, address):
    client = MongoClient('mongodb://localhost:27017/')  # replace with your MongoDB URI
    db = client['parking_spot']  # replace with your database name
    collection1 = db['users']  # replace with your collection name
    # add points to the user
    userDB= None
    resultUser = collection1.find({'email': email})
    for i in resultUser:
        print(i)
        userDB = i
        points = userDB['points']
        points += 2
        userDB['points'] = points
        collection1.update_one({'email': email}, {'$set': {'points': points}})
        break

    collection2 = db['parkings_kahol_lavan']  # replace with your collection name
    resultParking = collection2.find({'address': address})
    parkingDB=None
    print(resultParking)
    for i in resultParking:
        print(i)
        parkingDB = i
        collection2.update_one({'address': parkingDB['address']}, {'$set': {'release_time': "", 'status': 'תפוס', }})
        parkingDB['status']='תפוס'
        parkingDB['release_time']=""
        collection1.update_one({'email': email}, {'$set': {'parking': parkingDB}})
        userDB['parking'] = parkingDB
        break

    # Close MongoDB client
    client.close()
    print(userDB)
    print(parkingDB)
    return userDB, parkingDB


def get_user_points(user):
    client = MongoClient('mongodb://localhost:27017/')  # replace with your MongoDB URI
    db = client['parking_spot']  # replace with your database name
    collection = db['users']
    result = collection.find({'name': user['name'], 'email': user['email']})
    for i in result:
        print(i)
        user = i
    points = user['points']
    print(f"the result: {points}")
    return points


def user_exist_db(user):
    client = MongoClient('mongodb://localhost:27017/')  # replace with your MongoDB URI
    db = client['parking_spot']  # replace with your database name
    collection = db['users']
    result = collection.find({'name': user['name'], 'email': user['email']})
    print(f"the result: {result}")
    for i in result:
        print(i)
        if i is not None:
            client.close()
            return True
    client.close()
    return False

def user_exist_by_email_password(email, password):
    client = MongoClient('mongodb://localhost:27017/')  # replace with your MongoDB URI
    db = client['parking_spot']  # replace with your database name
    collection = db['users']
    result = collection.find({'email': email, 'password': password})
    for i in result:
        print(i)
        if i is not None:
            client.close()
            return True
    client.close()
    return False


def get_user_by_email_password(email, password):
    client = MongoClient('mongodb://localhost:27017/')  # replace with your MongoDB URI
    db = client['parking_spot']  # replace with your database name
    collection = db['users']
    result = collection.find({'email': email, 'password': password})
    user = None
    for i in result:
        print(i)
        user = i
        client.close()
        return user
    client.close()
    return user

#
# def get_user_by_email(email):
#     client = MongoClient('mongodb://localhost:27017/')  # replace with your MongoDB URI
#     db = client['parking_spot']  # replace with your database name
#     collection = db['users']
#     result = collection.find({'email': email})
#     user = None
#     for i in result:
#         print(i)
#         user = i
#         client.close()
#         return user
#     client.close()
#     return user


def get_parking_kl_by_address(address):
    client = MongoClient('mongodb://localhost:27017/')  # replace with your MongoDB URI
    db = client['parking_spot']  # replace with your database name
    collection = db['parkings_kahol_lavan']
    result = collection.find({'address': address})
    parking = None
    for i in result:
        print(i)
        parking = i
        client.close()
        return parking
    client.close()
    return parking


# def update_all_documents(collection_name, update_query):
#     """
#     Update all documents in the specified MongoDB collection.
#     :param collection_name: Name of the collection to update documents.
#     :param update_query: Update query to apply on all documents in the collection.
#     :return: None
#     """
#     client = MongoClient()  # Connect to default MongoDB server running on localhost
#     db = client.mydatabase  # Select the database to work with
#     collection = db[collection_name]  # Select the collection to update documents
#
#     result = collection.update_many({}, update_query)
#     print(f"Number of documents matched: {result.matched_count}")
#     print(f"Number of documents modified: {result.modified_count}")

def main():
    #insert_parking_kahol_lavan_data_to_mongodb()
    #insert_users_data_to_mongodb()
    #users_list = get_users_list()
    #get_user_points(users_list[0])
    kahol_lavan_list= get_parking_kahol_lavan_list()
    #update_parking_release(users_list[0]['email'],kahol_lavan_list[0]['address'])
    #users_list = get_users_list()
    #kahol_lavan_list= get_parking_kahol_lavan_list()
    #update_grabbing_parking(users_list[0]['email'], kahol_lavan_list[0]['address'])
    #update_parking_release_time(users_list[0]['email'],kahol_lavan_list[0]['address'],'14:40')
    #insert_parking_lot_data_to_mongodb()
    #result = get_user_by_email_password("avi@gmail.com","12345678")
    #print(result)

if __name__ == "__main__":
    # response = get_parking_lot_location(43)
    # print(response)
    main()
