import uuid

from rest_framework import status
from rest_framework.test import APITestCase

import api.tests.utils as test_utils


class BasicServiceTestCase(APITestCase):
    service_names = []

    def setUp(self):
        service_name = test_utils.get_random_name()
        self.service_names.append(service_name)
        create_data = {'name': service_name}

        test_utils.login_client(self.client, admin=True)
        self.create_service_test(status.HTTP_201_CREATED, create_data)
        self.client.logout()

    def get_services_test(self, expected_status):
        response = self.client.get('/api/service/', format='json')
        self.assertEqual(response.status_code, expected_status)
        return response

    def get_single_service_test(self, expected_status, service_oid):
        response = self.client.get(f'/api/service/{service_oid}/', format='json')
        self.assertEqual(response.status_code, expected_status)
        return response

    def create_service_test(self, expected_status, data):
        response = self.client.post('/api/service/', format='json', data=data)
        self.assertEqual(response.status_code, expected_status)
        return response

    def update_service_test(self, expected_status, service_oid, data):
        response = self.client.patch(f'/api/service/{service_oid}/', format='json', data=data)
        self.assertEqual(response.status_code, expected_status)
        return response

    def test_service_permissions(self):
        service_name = test_utils.get_random_name()
        self.service_names.append(service_name)
        bad_uuid = uuid.uuid4()
        create_data = {'name': service_name}
        update_data = {'name': f'{service_name}_updated'}

        self.get_services_test(status.HTTP_401_UNAUTHORIZED)
        self.get_single_service_test(status.HTTP_401_UNAUTHORIZED, bad_uuid)
        self.create_service_test(status.HTTP_401_UNAUTHORIZED, create_data)
        self.update_service_test(status.HTTP_401_UNAUTHORIZED, bad_uuid, update_data)

        test_utils.login_client(self.client)
        self.get_services_test(status.HTTP_200_OK)
        self.get_single_service_test(status.HTTP_404_NOT_FOUND, bad_uuid)
        self.create_service_test(status.HTTP_403_FORBIDDEN, create_data)
        self.update_service_test(status.HTTP_403_FORBIDDEN, bad_uuid, update_data)
        self.client.logout()

        test_utils.login_client(self.client, admin=True)
        self.get_services_test(status.HTTP_200_OK)
        response = self.create_service_test(status.HTTP_201_CREATED, create_data)
        self.get_single_service_test(status.HTTP_200_OK, response.data['oid'])
        self.update_service_test(status.HTTP_200_OK, response.data['oid'], update_data)
        self.client.logout()

    def test_service_lifecycle(self):
        bad_uuid = uuid.uuid4()
        test_utils.login_client(self.client, admin=True)
        service_name = test_utils.get_random_name()
        self.service_names.append(service_name)
        create_data = {'name': service_name}
        update_data = {'name': f'{service_name}_updated'}

        response = self.create_service_test(status.HTTP_201_CREATED, create_data)
        new_service_oid = response.data['oid']

        response = self.get_services_test(status.HTTP_200_OK)
        db_services = response.data
        self.assertEqual(len(db_services), len(self.service_names))
        self.assertIn(new_service_oid, [x['oid'] for x in db_services])

        response = self.get_single_service_test(status.HTTP_200_OK, new_service_oid)
        self.assertEqual(response.data['name'], create_data['name'])

        response = self.update_service_test(status.HTTP_200_OK, response.data['oid'], update_data)
        self.assertNotEqual(create_data['name'], response.data['name'])
        self.assertEqual(update_data['name'], response.data['name'])
        self.assertEqual(new_service_oid, response.data['oid'])

        # Test bad requests
        update_data['status'] = '42'
        response = self.update_service_test(status.HTTP_404_NOT_FOUND, bad_uuid, update_data)
        response = self.update_service_test(status.HTTP_400_BAD_REQUEST, new_service_oid,
                                            update_data)

        self.client.logout()
