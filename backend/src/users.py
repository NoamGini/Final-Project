from backend.src.parking_kahol_lavan import *
from backend.constants import *


def create_users_list():
    kahol_lavan_parking_list = generate_list_kahol_lavan()
    users_list = []
    users_list = get_users_list(users_list)

    for i in range(12, len(kahol_lavan_parking_list)):
        parking = kahol_lavan_parking_list[i]

        user = {
            EMAIL: f'user{i + 1}@gmail.com',
            NAME_SMALL_LETTER: f'User {i + 1}',
            PASSWORD: '12345678',
            PARKING: parking,
            POINTS: 5,
            AVATAR: None
        }

        users_list.append(user)

    return users_list


def get_users_list(users_list):
    parking10 = generate_list_kahol_lavan()[9]
    parking11 = generate_list_kahol_lavan()[10]
    user1 = {EMAIL: 'noam@gmail.com', NAME_SMALL_LETTER: 'Noam', PASSWORD: '12345678', PARKING: None, POINTS: 5,
             AVATAR: None}
    user2 = {EMAIL: 'noa@gmail.com', NAME_SMALL_LETTER: 'Noa', PASSWORD: '12345678', PARKING: parking11, POINTS: 5,
             AVATAR: None}
    user3 = {EMAIL: 'amit@gmail.com', NAME_SMALL_LETTER: 'Amit', PASSWORD: '12345678', PARKING: parking10, POINTS: 5,
             AVATAR: None}

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
