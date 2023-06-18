from parking_kahol_lavan import *



user_list=[]


def get_users_list():
    parking1 = get_parking_kahol_lavan_list()[0]
    parking2 = get_parking_kahol_lavan_list()[1]
    user1 = {'email':'noam@gmail.com', 'name': 'Noam Gini', 'password': '12345678', 'parking':parking1, 'points': 5, 'avatar': None }
    user2 = {'email':'noa@gmail.com', 'name': 'Noa Ziv', 'password': '12345678', 'parking':parking2, 'points': 5, 'avatar': None }
    user_list.append(user1)
    user_list.append(user2)
    return user_list


