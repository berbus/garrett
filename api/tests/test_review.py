import uuid

from rest_framework import status
from rest_framework.test import APITestCase

import api.tests.utils as test_utils
import api.models as models


class BasicReviewTestCase(APITestCase):
    review_names = []

    def setUp(self):
        self.service = models.Service(name='Test service')
        self.service.save()
        self.template = models.Template.objects.first()

        review_name = test_utils.get_random_name()
        self.review_names.append(review_name)
        create_data = {
            'title': review_name,
            'service': self.service.oid,
            'template': self.template.oid
        }

        test_utils.login_client(self.client, admin=True)
        self.create_review_test(status.HTTP_201_CREATED, create_data)
        self.client.logout()

    def get_reviews_test(self, expected_status):
        response = self.client.get('/api/review/', format='json')
        self.assertEqual(response.status_code, expected_status)
        return response

    def get_single_review_test(self, expected_status, review_oid):
        response = self.client.get(f'/api/review/{review_oid}/', format='json')
        self.assertEqual(response.status_code, expected_status)
        return response

    def create_review_test(self, expected_status, data):
        response = self.client.post('/api/review/', format='json', data=data)
        self.assertEqual(response.status_code, expected_status)
        return response

    def update_review_test(self, expected_status, review_oid, data):
        response = self.client.patch(f'/api/review/{review_oid}/', format='json', data=data)
        self.assertEqual(response.status_code, expected_status)
        return response

    def test_review_permissions(self):
        review_name = test_utils.get_random_name()
        self.review_names.append(review_name)
        bad_uuid = uuid.uuid4()
        create_data = {
            'title': review_name,
            'service': self.service.oid,
            'template': self.template.oid
        }
        update_data = {'title': f'{review_name}_updated'}

        self.get_reviews_test(status.HTTP_401_UNAUTHORIZED)
        self.get_single_review_test(status.HTTP_401_UNAUTHORIZED, bad_uuid)
        self.create_review_test(status.HTTP_401_UNAUTHORIZED, create_data)
        self.update_review_test(status.HTTP_401_UNAUTHORIZED, bad_uuid, update_data)

        test_utils.login_client(self.client)
        self.get_reviews_test(status.HTTP_200_OK)
        self.get_single_review_test(status.HTTP_404_NOT_FOUND, bad_uuid)
        self.create_review_test(status.HTTP_403_FORBIDDEN, create_data)
        self.update_review_test(status.HTTP_403_FORBIDDEN, bad_uuid, update_data)
        self.client.logout()

        test_utils.login_client(self.client, admin=True)
        self.get_reviews_test(status.HTTP_200_OK)
        response = self.create_review_test(status.HTTP_201_CREATED, create_data)
        self.get_single_review_test(status.HTTP_200_OK, response.data['oid'])
        self.update_review_test(status.HTTP_200_OK, response.data['oid'], update_data)
        self.client.logout()

    def test_review_lifecycle(self):
        bad_uuid = uuid.uuid4()
        test_utils.login_client(self.client, admin=True)
        review_name = test_utils.get_random_name()
        self.review_names.append(review_name)
        create_data = {
            'title': review_name,
            'service': self.service.oid,
            'template': self.template.oid
        }
        update_data = {'title': f'{review_name}_updated'}

        response = self.create_review_test(status.HTTP_201_CREATED, create_data)
        new_review_oid = response.data['oid']

        response = self.get_reviews_test(status.HTTP_200_OK)
        db_reviews = response.data
        self.assertEqual(len(db_reviews), len(self.review_names))
        self.assertIn(new_review_oid, [x['oid'] for x in db_reviews])

        response = self.get_single_review_test(status.HTTP_200_OK, new_review_oid)
        self.assertEqual(response.data['title'], create_data['title'])

        response = self.update_review_test(status.HTTP_200_OK, response.data['oid'], update_data)
        self.assertNotEqual(create_data['title'], response.data['title'])
        self.assertEqual(update_data['title'], response.data['title'])
        self.assertEqual(new_review_oid, response.data['oid'])

        # Test bad requests
        response = self.update_review_test(status.HTTP_404_NOT_FOUND, bad_uuid, update_data)

        self.client.logout()

    def tearDown(self):
        self.service.delete()
