import uuid

from rest_framework import status
from rest_framework.test import APITestCase

import api.tests.utils as test_utils



class BasicRequirementTestCase(APITestCase):
    requirement_rids = []

    def setUp(self):
        requirement_rid = test_utils.get_random_name()
        self.requirement_rids.append(requirement_rid)
        create_data = {'readable_id': requirement_rid, 'description': ''}

        test_utils.login_client(self.client, admin=True)
        self.create_requirement_test(status.HTTP_201_CREATED, create_data)
        self.client.logout()

    def get_requirements_test(self, expected_status):
        response = self.client.get('/api/requirement/', format='json')
        self.assertEqual(response.status_code, expected_status)
        return response

    def get_single_requirement_test(self, expected_status, requirement_oid):
        response = self.client.get(f'/api/requirement/{requirement_oid}/', format='json')
        self.assertEqual(response.status_code, expected_status)
        return response

    def create_requirement_test(self, expected_status, data):
        response = self.client.post('/api/requirement/', format='json', data=data)
        self.assertEqual(response.status_code, expected_status)
        return response

    def update_requirement_test(self, expected_status, requirement_oid, data):
        response = self.client.patch(f'/api/requirement/{requirement_oid}/', format='json', data=data)
        self.assertEqual(response.status_code, expected_status)
        return response

    def test_requirement_permissions(self):
        requirement_rid = test_utils.get_random_name()
        self.requirement_rids.append(requirement_rid)
        bad_uuid = uuid.uuid4()
        create_data = {'readable_id': requirement_rid, 'description': ''}
        update_data = {'readable_id': f'{requirement_rid}_updated'}

        self.get_requirements_test(status.HTTP_401_UNAUTHORIZED)
        self.get_single_requirement_test(status.HTTP_401_UNAUTHORIZED, bad_uuid)
        self.create_requirement_test(status.HTTP_401_UNAUTHORIZED, create_data)
        self.update_requirement_test(status.HTTP_401_UNAUTHORIZED, bad_uuid, update_data)

        test_utils.login_client(self.client)
        self.get_requirements_test(status.HTTP_200_OK)
        self.get_single_requirement_test(status.HTTP_404_NOT_FOUND, bad_uuid)
        self.create_requirement_test(status.HTTP_403_FORBIDDEN, create_data)
        self.update_requirement_test(status.HTTP_403_FORBIDDEN, bad_uuid, update_data)
        self.client.logout()

        test_utils.login_client(self.client, admin=True)
        self.get_requirements_test(status.HTTP_200_OK)
        response = self.create_requirement_test(status.HTTP_201_CREATED, create_data)
        self.get_single_requirement_test(status.HTTP_200_OK, response.data['oid'])
        self.update_requirement_test(status.HTTP_200_OK, response.data['oid'], update_data)
        self.client.logout()


    def test_requirement_lifecycle(self):
        bad_uuid = uuid.uuid4()
        test_utils.login_client(self.client, admin=True)
        requirement_rid = test_utils.get_random_name()
        self.requirement_rids.append(requirement_rid)
        create_data = {'readable_id': requirement_rid, 'description': ''}
        update_data = {'readable_id': f'{requirement_rid}_updated'}

        response = self.create_requirement_test(status.HTTP_201_CREATED, create_data)
        new_requirement_oid = response.data['oid']

        response = self.get_requirements_test(status.HTTP_200_OK)
        db_requirements = response.data
        self.assertIn(new_requirement_oid, [x['oid'] for x in db_requirements])

        response = self.get_single_requirement_test(status.HTTP_200_OK, new_requirement_oid)
        self.assertEqual(response.data['readable_id'], create_data['readable_id'])

        response = self.update_requirement_test(status.HTTP_200_OK, response.data['oid'], update_data)
        self.assertNotEqual(create_data['readable_id'], response.data['readable_id'])
        self.assertEqual(update_data['readable_id'], response.data['readable_id'])
        self.assertEqual(new_requirement_oid, response.data['oid'])

        # Test bad requests
        response = self.update_requirement_test(status.HTTP_404_NOT_FOUND, bad_uuid, update_data)

        self.client.logout()
