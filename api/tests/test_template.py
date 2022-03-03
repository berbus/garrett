import uuid

from rest_framework import status
from rest_framework.test import APITestCase

import api.tests.utils as test_utils



class BasicTemplateTestCase(APITestCase):
    template_names = []

    def setUp(self):
        template_name = test_utils.get_random_name()
        self.template_names.append(template_name)
        data = {'name': template_name}

        test_utils.login_client(self.client, admin=True)
        self.create_template_test(status.HTTP_201_CREATED, data)
        self.client.logout()

    def get_templates_test(self, expected_status):
        response = self.client.get('/api/template/', format='json')
        self.assertEqual(response.status_code, expected_status)
        return response

    def get_single_template_test(self, expected_status, template_oid):
        response = self.client.get(f'/api/template/{template_oid}/', format='json')
        self.assertEqual(response.status_code, expected_status)
        return response

    def create_template_test(self, expected_status, data):
        response = self.client.post('/api/template/', format='json', data=data)
        self.assertEqual(response.status_code, expected_status)
        return response

    def update_template_test(self, expected_status, template_oid, data):
        response = self.client.patch(f'/api/template/{template_oid}/', format='json', data=data)
        self.assertEqual(response.status_code, expected_status)
        return response

    def test_template_permissions(self):
        template_name = test_utils.get_random_name()
        self.template_names.append(template_name)
        bad_uuid = uuid.uuid4()
        create_data = {'name': template_name}
        update_data = {'name': f'{template_name}_updated'}

        self.get_templates_test(status.HTTP_401_UNAUTHORIZED)
        self.get_single_template_test(status.HTTP_401_UNAUTHORIZED, bad_uuid)
        self.create_template_test(status.HTTP_401_UNAUTHORIZED, create_data)
        self.update_template_test(status.HTTP_401_UNAUTHORIZED, bad_uuid, update_data)

        test_utils.login_client(self.client)
        self.get_templates_test(status.HTTP_200_OK)
        self.get_single_template_test(status.HTTP_404_NOT_FOUND, bad_uuid)
        self.create_template_test(status.HTTP_403_FORBIDDEN, create_data)
        self.update_template_test(status.HTTP_403_FORBIDDEN, bad_uuid, update_data)
        self.client.logout()

        test_utils.login_client(self.client, admin=True)
        self.get_templates_test(status.HTTP_200_OK)
        response = self.create_template_test(status.HTTP_201_CREATED, create_data)
        self.get_single_template_test(status.HTTP_200_OK, response.data['oid'])
        self.update_template_test(status.HTTP_200_OK, response.data['oid'], update_data)
        self.client.logout()


    def test_template_lifecycle(self):
        bad_uuid = uuid.uuid4()
        test_utils.login_client(self.client, admin=True)
        template_name = test_utils.get_random_name()
        self.template_names.append(template_name)
        create_data = {'name': template_name}
        update_data = {'name': f'{template_name}_updated'}

        response = self.create_template_test(status.HTTP_201_CREATED, create_data)
        new_template_oid = response.data['oid']

        response = self.get_templates_test(status.HTTP_200_OK)
        db_templates = response.data
        self.assertEqual(len(db_templates), len(self.template_names) + 3) # Add default templates
        self.assertIn(new_template_oid, [x['oid'] for x in db_templates])

        response = self.get_single_template_test(status.HTTP_200_OK, new_template_oid)
        self.assertEqual(response.data['name'], create_data['name'])

        response = self.update_template_test(status.HTTP_200_OK, response.data['oid'], update_data)
        self.assertNotEqual(create_data['name'], response.data['name'])
        self.assertEqual(update_data['name'], response.data['name'])
        self.assertEqual(new_template_oid, response.data['oid'])

        # Test bad requests
        response = self.update_template_test(status.HTTP_404_NOT_FOUND, bad_uuid, update_data)

        self.client.logout()
