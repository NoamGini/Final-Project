from backend.src.parking_kahol_lavan import *



user_list=[]


def get_users_list():
    parking1 = get_parking_kahol_lavan_list()[0]
    parking10 = get_parking_kahol_lavan_list()[9]
    parking11 = get_parking_kahol_lavan_list()[10]
    user1 = {'email':'noam@gmail.com', 'name': 'Noam', 'password': '12345678', 'parking':None, 'points': 5, 'avatar': None }
    user2 = {'email':'noa@gmail.com', 'name': 'Noa', 'password': '12345678', 'parking':parking10, 'points': 5, 'avatar': None }
    user3 = {'email':'amit@gmail.com', 'name': 'Amit', 'password': '12345678', 'parking':parking11, 'points': 5, 'avatar': None }

    user_list.append(user1)
    user_list.append(user2)
    user_list.append(user3)
    return user_list


