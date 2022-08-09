import uuid

from rest_framework import status
from rest_framework.test import APITestCase

import api.models as models
import api.tests.utils as test_utils


class BasicFindingTestCase(APITestCase):
    finding_names = []

    def setUp(self):
        self.service = models.Service(name='Test service')
        self.service.save()
        aux_template = models.Template.objects.first()
        aux_requirement = models.Requirement.objects.first()
        self.review = models.Review(title='Test review',
                                        service=self.service,
                                        template=aux_template)
        self.review.save()
        self.test_case = models.TestCase(review=self.review, requirement=aux_requirement)
        self.test_case.save()

        finding_name = test_utils.get_random_name()
        self.finding_names.append(finding_name)
        create_data = {
            'title': finding_name,
            'test_case': self.test_case.oid,
            'review': self.review.oid
        }

        test_utils.login_client(self.client, admin=True)
        self.create_finding_test(status.HTTP_201_CREATED, create_data)
        self.client.logout()

    def get_findings_test(self, expected_status):
        response = self.client.get('/api/finding/', format='json')
        self.assertEqual(response.status_code, expected_status)
        return response

    def get_single_finding_test(self, expected_status, finding_oid):
        response = self.client.get(f'/api/finding/{finding_oid}/', format='json')
        self.assertEqual(response.status_code, expected_status)
        return response

    def create_finding_test(self, expected_status, data):
        response = self.client.post('/api/finding/', format='json', data=data)
        self.assertEqual(response.status_code, expected_status)
        return response

    def update_finding_test(self, expected_status, finding_oid, data):
        response = self.client.patch(f'/api/finding/{finding_oid}/', format='json', data=data)
        self.assertEqual(response.status_code, expected_status)
        return response

    def test_finding_permissions(self):
        finding_name = test_utils.get_random_name()
        self.finding_names.append(finding_name)
        bad_uuid = uuid.uuid4()
        create_data = {
            'title': finding_name,
            'test_case': self.test_case.oid,
            'review': self.review.oid
        }
        update_data = {'title': f'{finding_name}_updated'}

        self.get_findings_test(status.HTTP_401_UNAUTHORIZED)
        self.get_single_finding_test(status.HTTP_401_UNAUTHORIZED, bad_uuid)
        self.create_finding_test(status.HTTP_401_UNAUTHORIZED, create_data)
        self.update_finding_test(status.HTTP_401_UNAUTHORIZED, bad_uuid, update_data)

        test_utils.login_client(self.client)
        self.get_findings_test(status.HTTP_200_OK)
        self.get_single_finding_test(status.HTTP_404_NOT_FOUND, bad_uuid)
        self.create_finding_test(status.HTTP_403_FORBIDDEN, create_data)
        self.update_finding_test(status.HTTP_403_FORBIDDEN, bad_uuid, update_data)
        self.client.logout()

        test_utils.login_client(self.client, admin=True)
        self.get_findings_test(status.HTTP_200_OK)
        response = self.create_finding_test(status.HTTP_201_CREATED, create_data)
        self.get_single_finding_test(status.HTTP_200_OK, response.data['oid'])
        self.update_finding_test(status.HTTP_200_OK, response.data['oid'], update_data)
        self.client.logout()

    def test_finding_lifecycle(self):
        bad_uuid = uuid.uuid4()
        test_utils.login_client(self.client, admin=True)
        finding_name = test_utils.get_random_name()
        self.finding_names.append(finding_name)
        create_data = {
            'title': finding_name,
            'test_case': self.test_case.oid,
            'review': self.review.oid
        }
        update_data = {'title': f'{finding_name}_updated'}

        response = self.create_finding_test(status.HTTP_201_CREATED, create_data)
        new_finding_oid = response.data['oid']

        response = self.get_findings_test(status.HTTP_200_OK)
        db_findings = response.data
        self.assertEqual(len(db_findings), len(self.finding_names))
        self.assertIn(new_finding_oid, [x['oid'] for x in db_findings])

        response = self.get_single_finding_test(status.HTTP_200_OK, new_finding_oid)
        self.assertEqual(response.data['title'], create_data['title'])

        response = self.update_finding_test(status.HTTP_200_OK, response.data['oid'], update_data)
        self.assertNotEqual(create_data['title'], response.data['title'])
        self.assertEqual(update_data['title'], response.data['title'])
        self.assertEqual(new_finding_oid, response.data['oid'])

        # Test bad requests
        response = self.update_finding_test(status.HTTP_404_NOT_FOUND, bad_uuid, update_data)

        self.client.logout()

    def tearDown(self):
        self.service.delete()
        self.review.delete()
        self.test_case.delete()
