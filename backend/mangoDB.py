import pymongo
from getDataFromURL import *
from getDataFromAPI import *
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

def insert_data_to_mongodb():
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


def user_exist_db(user):
    client = MongoClient('mongodb://localhost:27017/')  # replace with your MongoDB URI
    db = client['parking_spot']  # replace with your database name
    collection = db['users']
    result = collection.find({'name': user['name'], 'email': user['email']})
    print(f"the result: {result}")
    for i in result:
        print(i)
        if i is not None:
            return True
    return False

def user_exist_by_email_password(email, password):
    client = MongoClient('mongodb://localhost:27017/')  # replace with your MongoDB URI
    db = client['parking_spot']  # replace with your database name
    collection = db['users']
    result = collection.find({'email': email, 'password': password})
    for i in result:
        print(i)
        if i is not None:
            return True
    return False
#
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
    insert_data_to_mongodb()


if __name__ == "__main__":
    # response = get_parking_lot_location(43)
    # print(response)
    main()
