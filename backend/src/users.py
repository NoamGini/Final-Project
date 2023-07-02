from backend.src.parking_kahol_lavan import *


def create_users_list():
    kahol_lavan_parking_list = generate_list_kahol_lavan()
    users_list = []
    users_list = get_users_list(users_list)

    for i in range(12, len(kahol_lavan_parking_list)):
        parking = kahol_lavan_parking_list[i]

        user = {
            'email': f'user{i + 1}@gmail.com',
            'name': f'User {i + 1}',
            'password': '12345678',
            'parking': parking,
            'points': 5,
            'avatar': None
        }

        users_list.append(user)

    return users_list


def get_users_list(users_list):
    parking10 = generate_list_kahol_lavan()[9]
    parking11 = generate_list_kahol_lavan()[10]
    user1 = {'email': 'noam@gmail.com', 'name': 'Noam', 'password': '12345678', 'parking': None, 'points': 5,
             'avatar': None}
    user2 = {'email': 'noa@gmail.com', 'name': 'Noa', 'password': '12345678', 'parking': parking10, 'points': 5,
             'avatar': None}
    user3 = {'email': 'amit@gmail.com', 'name': 'Amit', 'password': '12345678', 'parking': parking11, 'points': 5,
             'avatar': None}

    users_list.append(user1)
    users_list.append(user2)
    users_list.append(user3)
    return users_list


def main():
    users_list = create_users_list()
    for user in users_list:
        print(user)


if __name__ == '__main__':
    main()