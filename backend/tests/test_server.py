from unittest import mock
from flask_testing import TestCase
from unittest.mock import patch
from backend.src.server import *


class ServerTestCase(TestCase):
    def create_app(self):
        return app

    def test_get_all_parking_lots(self):
        with patch('backend.src.server.get_all_data_from_collection_hauzot') as mock_get_collection_hauzot, \
                patch('backend.src.server.get_all_data_from_collection_central') as mock_get_collection_central:
            mock_get_collection_hauzot.return_value = [{'name': 'Parking Lot 1'}, {'name': 'Parking Lot 2'}]
            mock_get_collection_central.return_value = [{'name': 'Parking Lot 3'}, {'name': 'Parking Lot 4'}]

            response = self.client.get('/closest_parking/')

            self.assert200(response)
            data = json.loads(response.data.decode('utf-8'))
            self.assertEqual(data, [{'name': 'Parking Lot 1'}, {'name': 'Parking Lot 2'},
                                    {'name': 'Parking Lot 3'}, {'name': 'Parking Lot 4'}])

    @mock.patch('backend.src.server.global_parking_lots_by_address')
    @mock.patch('backend.src.server.get_all_data_from_collection_hauzot')
    @mock.patch('backend.src.server.get_all_data_from_collection_central')
    @mock.patch('backend.src.server.get_closest_parking_by_address_hauzot')
    @mock.patch('backend.src.server.get_closest_parking_by_address')
    def test_get_closest_parking_by_address_from_client(
            self,
            mock_get_closest_parking_by_address,
            mock_get_closest_parking_by_address_hauzot,
            mock_get_all_data_from_collection_central,
            mock_get_all_data_from_collection_hauzot,
            mock_global_parking_lots_by_address
    ):
        # Mock the return values of the database functions
        mock_get_closest_parking_by_address.return_value = [
            ({'name': 'Parking Lot 14', 'address': '14 Main St'}, 513, '7 mins'),
            ({'name': 'Parking Lot 13', 'address': '13 Main St'}, 1695, '22 mins')]
        mock_get_all_data_from_collection_hauzot.return_value = [
            {'name': 'Parking Lot 10', 'address': '10 Main St'},
            {'name': 'Parking Lot 12', 'address': '12 Main St'}]
        mock_get_all_data_from_collection_central.return_value = [
            {'name': 'Parking Lot 14', 'address': '14 Main St'},
            {'name': 'Parking Lot 13', 'address': '13 Main St'}]
        mock_get_closest_parking_by_address_hauzot.return_value = [
            ({'name': 'Parking Lot 12', 'address': '12 Main St'}, 1836, '23 mins'),
            ({'name': 'Parking Lot 10', 'address': '10 Main St'}, 1901, '25 mins')]
        mock_global_parking_lots_by_address.return_value = [
            ({'name': 'Parking Lot 14', 'address': '14 Main St'}, 513, '7 mins'),
            ({'name': 'Parking Lot 13', 'address': '13 Main St'}, 1695, '22 mins'),
            ({'name': 'Parking Lot 12', 'address': '12 Main St'}, 1836, '23 mins'),
            ({'name': 'Parking Lot 10', 'address': '10 Main St'}, 1901, '25 mins')]

        # Make a request to the endpoint
        response = self.client.get('/closest_parking/141 Main St')

        # Assert the response status code
        assert response.status_code == 200

        # Assert the response data
        expected_data = json.dumps(mock_global_parking_lots_by_address.return_value, ensure_ascii=False,
                                   default=str).encode('utf8')
        print(response.data)
        print(expected_data)
        assert response.data == expected_data

        # Assert that the database functions were called with the correct arguments
        mock_get_all_data_from_collection_hauzot.assert_called_once()
        mock_get_all_data_from_collection_central.assert_called_once()
        mock_get_closest_parking_by_address_hauzot.assert_called_once()
        mock_get_closest_parking_by_address.assert_called_once()

    def test_get_closest_parking_by_distance_specified_by_client(self):
        mock_parking_lots = [
            ({'name': 'Parking Lot 14', 'address': '14 Main St'}, 513, '7 mins'),
            ({'name': 'Parking Lot 13', 'address': '13 Main St'}, 1695, '22 mins'),
            ({'name': 'Parking Lot 12', 'address': '12 Main St'}, 1836, '23 mins'),
            ({'name': 'Parking Lot 10', 'address': '10 Main St'}, 1901, '25 mins')
        ]

        with patch('backend.src.server.global_parking_lots_by_address', mock_parking_lots):
            response = self.client.get('/closest_parking/141 Main St/1700')

            return_list_data = [
                ({'name': 'Parking Lot 14', 'address': '14 Main St'}, 513, '7 mins'),
                ({'name': 'Parking Lot 13', 'address': '13 Main St'}, 1695, '22 mins')
            ]

            # Assert the response data
            expected_data = json.dumps(return_list_data, ensure_ascii=False, default=str).encode('utf8')

            self.assert200(response)
            print('3\n')
            print(response.data)
            print('4\n')
            print(expected_data)
            assert response.data == expected_data

    def test_get_closest_parking_by_duration_specified_by_client(self):
        mock_parking_lots = [
            ({'name': 'Parking Lot 14', 'address': '14 Main St'}, 513, '7 mins'),
            ({'name': 'Parking Lot 13', 'address': '13 Main St'}, 1695, '22 mins'),
            ({'name': 'Parking Lot 12', 'address': '12 Main St'}, 1836, '23 mins'),
            ({'name': 'Parking Lot 10', 'address': '10 Main St'}, 1901, '25 mins')
        ]

        with patch('backend.src.server.global_parking_lots_by_address', mock_parking_lots):
            response = self.client.get('/closest_parking_duration/141 Main St/23 mins')

            return_list_data = [
                ({'name': 'Parking Lot 14', 'address': '14 Main St'}, 513, '7 mins'),
                ({'name': 'Parking Lot 13', 'address': '13 Main St'}, 1695, '22 mins'),
                ({'name': 'Parking Lot 12', 'address': '12 Main St'}, 1836, '23 mins'),
            ]

            # Assert the response data
            expected_data = json.dumps(return_list_data, ensure_ascii=False, default=str).encode('utf8')

            self.assert200(response)
            print('3\n')
            print(response.data)
            print('4\n')
            print(expected_data)
            assert response.data == expected_data

    def test_get_parking_by_company(self):
        mock_parking_lots = [
            ({'name': 'Parking Lot 14', 'address': '14 Main St', 'AhuzotCode': 'Code 1'}, 513, '7 mins'),
            ({'name': 'Parking Lot 13', 'address': '13 Main St', 'AhuzotCode': 'Code 2'}, 1695, '22 mins'),
            ({'name': 'Parking Lot 12', 'address': '12 Main St', 'CentralParkCode': 'Code 3'}, 1836, '23 mins'),
            ({'name': 'Parking Lot 10', 'address': '10 Main St', 'CentralParkCode': 'Code 4'}, 1901, '25 mins')
        ]

        with patch('backend.src.server.global_parking_lots_by_address', mock_parking_lots):
            response = self.client.get('/closest_parking_company/141 Main St/אחוזת החוף')

            return_list_data = [
                ({'name': 'Parking Lot 14', 'address': '14 Main St', 'AhuzotCode': 'Code 1'}, 513, '7 mins'),
                ({'name': 'Parking Lot 13', 'address': '13 Main St', 'AhuzotCode': 'Code 2'}, 1695, '22 mins')
            ]

            # Assert the response data
            expected_data = json.dumps(return_list_data, ensure_ascii=False, default=str).encode('utf8')

            self.assert200(response)
            print('3\n')
            print(response.data)
            print('4\n')
            print(expected_data)
            assert response.data == expected_data

    def test_get_parking_by_status(self):
        mock_parking_lots = [
            ({'name': 'Parking Lot 14', 'address': '14 Main St', 'InformationToShow': "free"}, 513, '7 mins'),
            ({'name': 'Parking Lot 13', 'address': '13 Main St', 'InformationToShow': "few"}, 1695, '22 mins'),
            ({'name': 'Parking Lot 12', 'address': '12 Main St', 'InformationToShow': "free"}, 1836, '23 mins'),
            ({'name': 'Parking Lot 10', 'address': '10 Main St', 'InformationToShow': "full"}, 1901, '25 mins')
        ]

        with patch('backend.src.server.global_parking_lots_by_address', mock_parking_lots):
            response = self.client.get('/closest_parking_status/141 Main St/free')

            return_list_data = [
                ({'name': 'Parking Lot 14', 'address': '14 Main St', 'InformationToShow': "free"}, 513, '7 mins'),
                ({'name': 'Parking Lot 12', 'address': '12 Main St', 'InformationToShow': "free"}, 1836, '23 mins')
            ]

            # Assert the response data
            expected_data = json.dumps(return_list_data, ensure_ascii=False, default=str).encode('utf8')

            self.assert200(response)
            print('3\n')
            print(response.data)
            print('4\n')
            print(expected_data)
            assert response.data == expected_data

    @mock.patch('backend.src.server.get_all_data_from_collection_hauzot')
    @mock.patch('backend.src.server.get_all_data_from_collection_central')
    def test_get_parking_by_name(self, mock_get_all_data_from_collection_central,
                                 mock_get_all_data_from_collection_hauzot):
        mock_get_all_data_from_collection_hauzot.return_value = [
            {'Name': 'Parking Lot 10', 'address': '10 Main St'},
            {'Name': 'Parking Lot 12', 'address': '12 Main St'}]
        mock_get_all_data_from_collection_central.return_value = [
            {'Name': 'Parking Lot 14', 'address': '14 Main St'},
            {'Name': 'Parking Lot 13', 'address': '13 Main St'}]
        with self.app.test_request_context('/closest_parking_by_parking_name/Parking Lot 14'):
            response = get_parking_by_name("Parking Lot 14")

            expected_data = b'{"Name": "Parking Lot 14", "address": "14 Main St"}'
            self.assertEqual(response, expected_data)

        with self.app.test_request_context('/closest_parking_by_parking_name/Non-existent Parking Lot'):
            response = get_parking_by_name("Non-existent Parking Lot")

            expected_data = 'None'
            self.assertEqual(response, expected_data)

    def test_register(self):
        with patch('backend.src.server.add_user_to_db') as mock_add_user_to_db:
            mock_add_user_to_db.return_value = None

            # Mock request data
            request_data = {
                'name': 'Test User',
                'email': 'test@example.com',
                'password': 'password',
                'parking': 'parking_lot',
                'points': 0,
                'avatar': 'avatar.jpg'
            }

            # Send a mock request to the register route
            response = self.client.post('/register', json=request_data)

            self.assert200(response)
            self.assertEqual(response.json, {'response': 'User registered successfully'})
            mock_add_user_to_db.assert_called_once_with(request_data)

    @patch('backend.src.server.user_exist_by_email_password')
    def test_sign_in(self, mock_user_exist):
        # Configure the mock return value
        mock_user_exist.return_value = True

        # Make a POST request to the route
        response = self.client.post('/signIn', json={'email': 'test@example.com', 'password': 'password'})

        # Verify the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'response': 'exist'})

    def test_get_user(self):
        # Mock the database operation to simulate a response
        with patch('backend.src.server.get_user_by_email_password') as mock_get_user:
            # Set the return value of the mocked function
            mock_get_user.return_value = {'email': 'test@example.com', 'password': 'password'}

            # Make a request to the endpoint
            response = self.client.post('/signInGet', json={'email': 'test@example.com', 'password': 'password'})

            # Assertions
            self.assert200(response)
            self.assertEqual(response.get_data(as_text=True), '{"email": "test@example.com", "password": "password"}')

    def test_update_release_time(self):
        with self.app.test_client():
            with patch('backend.src.server.update_parking_release_time') as mock_update_parking_release_time:
                # Mock the database operation to return the desired response
                mock_update_parking_release_time.return_value = ('mock_user', 'mock_parking')

                # Make a test request to the route
                response = self.client.post('/parking_kahol_lavan/release_time', json={
                    'email': 'test@example.com',
                    'address': '123 Main St',
                    'release_time': '10:00 AM'
                })

                # Assertions
                assert response.status_code == 200
                self.assertEqual(response.data.decode('utf8'), '"mock_user"')

                # Verify that the mock function was called with the expected arguments
                mock_update_parking_release_time.assert_called_with('test@example.com', '123 Main St', '10:00 AM')

    # Mock the update_grabbing_parking function
    def test_update_grabbed_parking(self):
        with patch('backend.src.server.update_grabbing_parking') as mock_update_grabbing_parking:
            mock_update_grabbing_parking.return_value = 'mocked user', 'mocked parking'  # Set up the mock behavior

            response = self.client.post('/parking_kahol_lavan/grabbing_parking',
                                        json={
                                            'email': 'test@example.com',
                                            'address': '123 Street'
                                        })

        # Assert the expected behavior
        print(response)
        assert response.status_code == 200
        response_data = response.data.decode('utf8')
        response_without_quotes = response_data.strip('"')
        assert response_without_quotes == 'mocked user', 'mocked parking'

    @patch('backend.src.server.get_user_points')  # Mocking the get_user_points function
    def test_get_points(self, mock_get_user_points):
        # Configure the mock return value
        mock_get_user_points.return_value = 10

        response = self.client.post('/parking_kahol_lavan/points', json={'user': 'testuser'})

        # Assert the response
        self.assertEqual(response.status_code, 200)
        response_data = response.data.decode('utf8')
        response_without_quotes = int(response_data.strip('"'))
        self.assertEqual(response_without_quotes, 10)

    @patch('backend.src.server.update_parking_release')
    def test_update_release_parking(self, mock_update_parking_release):
        # Mock the database functions
        mock_update_parking_release.return_value = 'User updated', 'Parking updated'

        # Make a test request to the route
        response = self.client.post('/parking_kahol_lavan/release_parking',
                                    json={'email': 'example@example.com', 'address': '123 Main St.'})

        # Perform assertions on the response
        self.assertEqual(response.status_code, 200)
        response_data = response.data.decode('utf8')
        response_without_quotes = response_data.strip('"')
        self.assertEqual(response_without_quotes, 'User updated', 'Parking updated')
        mock_update_parking_release.assert_called_once_with('example@example.com', '123 Main St.')
