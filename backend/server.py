from flask import Flask
from getDataFromAPI import *
from getDataFromURL import *
import json
from mangoDB import *

flag = 0
app = Flask(__name__)
global_parking_lots_by_address = []
global_parking_lots_info = []


@app.route('/closest_parking/')
def get_all_parking_lots():
    global global_parking_lots_info
    TLV_parking_list_hauzot = get_all_data_from_collection_hauzot()
    # TLV_parking_names = get_parking_list()
    # TLV_parking_list_central = get_all_parking_lots_info(TLV_parking_names)
    TLV_parking_list_central = get_all_data_from_collection_central()
    all_parking_info = TLV_parking_list_hauzot + TLV_parking_list_central
    global_parking_lots_info = all_parking_info
    all_parking_info = json.dumps(all_parking_info, ensure_ascii=False, default=str).encode('utf8')
    return all_parking_info


@app.route('/closest_parking/<address>')
def get_closest_parking_by_address_from_client(address):
    global flag, global_parking_lots_by_address, global_parking_lots_info
    print("entered hauzot")
    TLV_parking_list_hauzot = get_all_data_from_collection_hauzot()
    response_hauzot = get_closest_parking_by_address_hauzot(TLV_parking_list_hauzot, address)
    print("finish hauzot")
    TLV_parking_list_central = get_all_data_from_collection_central()
    response_central = get_closest_parking_by_address(TLV_parking_list_central, address)
    print("finish central")
    # need to use this response in code
    response = response_hauzot + response_central
    print(response)
    response = sorted(response, key=lambda x: x[1])
    ten_parking_lots = response[:10]
    for parking in ten_parking_lots:
        if "AhuzotCode" in parking[0]:
            #update status in hauzot-ahof parking
            print("enter to update hauzot")
            updated_parking_hauzot = update_status(parking[0],parking[0]['AhuzotCode'])
            parking[0]['InformationToShow']=updated_parking_hauzot['InformationToShow']
            #update the db
            filter_query = {'Name': parking[0]['Name']}
            update_query = {'$set': {'InformationToShow': updated_parking_hauzot['InformationToShow']}}
            update_document("hauzot_ahof", filter_query, update_query)
            print("finish update db hauzot")
        else:
            print("enter to update central")
            updated_parking_central =update_parking_lot_status(parking)
            parking[0]['InformationToShow'] = updated_parking_central[0]['InformationToShow']
            filter_query = {'Name': updated_parking_central[0]['Name']}
            update_query = {'$set': {'InformationToShow': updated_parking_central[0]['InformationToShow']}}
            update_document("central_park", filter_query, update_query)
            print("finish update db central")

        global_parking_lots_by_address = ten_parking_lots
    ten_parking_lots = json.dumps(ten_parking_lots, ensure_ascii=False, default=str).encode('utf8')
    flag = 0
    #print(global_parking_lots_by_address)
    return ten_parking_lots


@app.route('/closest_parking/<address>/<distance>', endpoint='func2')
def get_closest_parking_by_distance_specified_by_client(address, distance):
    # don't need this call if the client opens first the main page which is this function and then picks distance filter
    # get_closest_parking_by_address_from_client(address)
    # closest_parking_lots = get_closest_parking_by_address_hauzot(address)
    # closest_parking_lot_by_distance = get_closest_parking_by_distance_hauzot(closest_parking_lots,distance)
    parking_filtered_by_distance = [tup for tup in global_parking_lots_by_address if tup[1] <= int(distance)]
    closest_parking_lot_by_distance = json.dumps(parking_filtered_by_distance, ensure_ascii=False, default=str).encode(
        'utf8')
    return closest_parking_lot_by_distance


@app.route('/closest_parking_duration/<address>/<duration>')
def get_closest_parking_by_duration_specified_by_client(address, duration):
    global global_parking_lots_by_address
    # don't need this call if the client opens first the main page which is this function and then picks distance filter
    # get_closest_parking_by_address_from_client
    #delete after
    #global_parking_lots_by_address = array
    #parking_filtered_by_duration = [tup for tup in global_parking_lots_by_address if tup[2] <= int(duration)]
    parking_filtered_by_duration = get_closest_parking_by_duration(global_parking_lots_by_address,duration)
    parking_filtered_by_duration = json.dumps(parking_filtered_by_duration, ensure_ascii=False, default=str).encode(
        'utf8')
    return parking_filtered_by_duration


@app.route('/closest_parking_company/<address>/<company>', endpoint='func1')
def get_parking_by_company(address, company):
    global flag
    response=[]
    if company == "אחוזת החוף":
        flag = 1
        for parking in global_parking_lots_by_address:
            if "AhuzotCode" in parking[0]:
                response.append(parking)
    if company == "סנטרל פארק":
        #maybe don't need the flag
        flag = 2
        for parking in global_parking_lots_by_address:
            if "CentralParkCode" in parking[0]:
                response.append(parking)

    response = json.dumps(response, ensure_ascii=False, default=str).encode('utf8')
    #parking_lots = get_closest_parking_by_address_from_client(address)
    return response


@app.route('/closest_parking_status/<address>/<status>')
def get_parking_by_status(address, status):
    # TLV_parking_list = get_parking_list()
    # response_central = get_closest_parking_by_address(TLV_parking_list, address)
    parking_lots_by_status = [tup for tup in global_parking_lots_by_address if tup[0]['InformationToShow'] == status]
    parking_lots_by_status = json.dumps(parking_lots_by_status, ensure_ascii=False, default=str).encode(
        'utf8')
    return parking_lots_by_status
    # if status == "פנוי":
    #     parking_lots_panui = all_free_parking_lots()
    #     parking_lots_panui += get_available_parking_lots(response_central)
    #     return parking_lots_panui
    # if status == "מעט":
    #     parking_lots_mehat = all_few_parking_lots_left()
    #     parking_lots_mehat += get_few_available_parking_lots(response_central)
    #     return parking_lots_mehat


@app.route('/closest_parking_by_parking_name/<parking_name>')
def get_parking_by_name(parking_name):
    print(global_parking_lots_info)
    for park in global_parking_lots_info:
        #print(park['Name'])
        if park['Name'] == parking_name:
            if "AhuzotCode" in park:
                #update status in hauzot-ahof parking
                update_status(park,park['AhuzotCode'])
            else:
                tuple = (park,"")
                update_parking_lot_status(tuple)
            park = json.dumps(park, ensure_ascii=False, default=str).encode('utf8')
            return park
    return "None"
    # name = get_parking_info_by_name(parking_name)
    # if name is not None:
    #     return name
    # else:
    #     name= get_parking_lot_info(parking_name)
    #     if name is not None:
    #         return name
    # return "Not found"


if __name__ == "__main__":
    # response = get_parking_lot_location(43)
    # print(response)
    app.run()
