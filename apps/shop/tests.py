import requests
from decouple import config
from django.test import TestCase
from rest_framework import status


class MyAPITestCase(TestCase):

    def test_empoyee_statistics(self):
        response = requests.get(f'{config("PRODUCTION_HOST")}employee/statistics/?month=11&year=2023', )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_statistics_with_pk(self):
        response = requests.get(f'{config("PRODUCTION_HOST")}statistics/employee/1?month=11&year=2023', )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_statistics_with_pk(self):
        response = requests.get(f'{config("PRODUCTION_HOST")}statistics/client/1?month=11&year=2023', )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
