import uuid

from rest_framework import status
from rest_framework.test import APITestCase

import api.tests.utils as test_utils
import api.models as models


class BasicExerciseTestCase(APITestCase):
    exercise_names = []

    def setUp(self):
        self.service = models.Service(name='Test service')
        self.service.save()
        self.template = models.Template.objects.first()

        exercise_name = test_utils.get_random_name()
        self.exercise_names.append(exercise_name)
        create_data = {
            'title': exercise_name,
            'service': self.service.oid,
            'template': self.template.oid
        }

        test_utils.login_client(self.client, admin=True)
        self.create_exercise_test(status.HTTP_201_CREATED, create_data)
        self.client.logout()

    def get_exercises_test(self, expected_status):
        response = self.client.get('/api/exercise/', format='json')
        self.assertEqual(response.status_code, expected_status)
        return response

    def get_single_exercise_test(self, expected_status, exercise_oid):
        response = self.client.get(f'/api/exercise/{exercise_oid}/', format='json')
        self.assertEqual(response.status_code, expected_status)
        return response

    def create_exercise_test(self, expected_status, data):
        response = self.client.post('/api/exercise/', format='json', data=data)
        self.assertEqual(response.status_code, expected_status)
        return response

    def update_exercise_test(self, expected_status, exercise_oid, data):
        response = self.client.patch(f'/api/exercise/{exercise_oid}/', format='json', data=data)
        self.assertEqual(response.status_code, expected_status)
        return response

    def test_exercise_permissions(self):
        exercise_name = test_utils.get_random_name()
        self.exercise_names.append(exercise_name)
        bad_uuid = uuid.uuid4()
        create_data = {
            'title': exercise_name,
            'service': self.service.oid,
            'template': self.template.oid
        }
        update_data = {'title': f'{exercise_name}_updated'}

        self.get_exercises_test(status.HTTP_401_UNAUTHORIZED)
        self.get_single_exercise_test(status.HTTP_401_UNAUTHORIZED, bad_uuid)
        self.create_exercise_test(status.HTTP_401_UNAUTHORIZED, create_data)
        self.update_exercise_test(status.HTTP_401_UNAUTHORIZED, bad_uuid, update_data)

        test_utils.login_client(self.client)
        self.get_exercises_test(status.HTTP_200_OK)
        self.get_single_exercise_test(status.HTTP_404_NOT_FOUND, bad_uuid)
        self.create_exercise_test(status.HTTP_403_FORBIDDEN, create_data)
        self.update_exercise_test(status.HTTP_403_FORBIDDEN, bad_uuid, update_data)
        self.client.logout()

        test_utils.login_client(self.client, admin=True)
        self.get_exercises_test(status.HTTP_200_OK)
        response = self.create_exercise_test(status.HTTP_201_CREATED, create_data)
        self.get_single_exercise_test(status.HTTP_200_OK, response.data['oid'])
        self.update_exercise_test(status.HTTP_200_OK, response.data['oid'], update_data)
        self.client.logout()

    def test_exercise_lifecycle(self):
        bad_uuid = uuid.uuid4()
        test_utils.login_client(self.client, admin=True)
        exercise_name = test_utils.get_random_name()
        self.exercise_names.append(exercise_name)
        create_data = {
            'title': exercise_name,
            'service': self.service.oid,
            'template': self.template.oid
        }
        update_data = {'title': f'{exercise_name}_updated'}

        response = self.create_exercise_test(status.HTTP_201_CREATED, create_data)
        new_exercise_oid = response.data['oid']

        response = self.get_exercises_test(status.HTTP_200_OK)
        db_exercises = response.data
        self.assertEqual(len(db_exercises), len(self.exercise_names))
        self.assertIn(new_exercise_oid, [x['oid'] for x in db_exercises])

        response = self.get_single_exercise_test(status.HTTP_200_OK, new_exercise_oid)
        self.assertEqual(response.data['title'], create_data['title'])

        response = self.update_exercise_test(status.HTTP_200_OK, response.data['oid'], update_data)
        self.assertNotEqual(create_data['title'], response.data['title'])
        self.assertEqual(update_data['title'], response.data['title'])
        self.assertEqual(new_exercise_oid, response.data['oid'])

        # Test bad requests
        response = self.update_exercise_test(status.HTTP_404_NOT_FOUND, bad_uuid, update_data)

        self.client.logout()

    def tearDown(self):
        self.service.delete()
