from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test  import APITestCase, APIClient
from wall.models import Message
from django.urls import reverse
from knox.models import AuthToken

class MessageTests(APITestCase):
    def setUp(self):
        self.username = 'john_doe'
        self.password = 'foobar'
        self.user = User.objects.create(username=self.username, password=self.password)
        self.client.force_authenticate(user=self.user)

    def test_message(self):
        response = self.client.post('/message/', {'title': 'Foo Bar', 'description': 'olaaa'}, format='json')
        self.assertEqual(response.status_code, 201)


class RegistrationTest(APITestCase):
    def test_registration(self):
        data = {
        "username": "ray", "email": "jj@gmail.com", "password": "jjjui"
        }
        response = self.client.post("127.0.0.1:8000/register", data)
        self.assertEqual(response.status_code, 201)


# class LogInTest(APITestCase):
#     def setUp(self):
#         self.credentials = {
#             'username': 'Kevin',
#             'password': 'aa'}
#         User.objects.create_user(**self.credentials)
#         self.token = AuthToken.objects.create(user=self.credentials)
#     def test_login(self):
#         client = APIClient()
#         client.login(username='Kevin', password='aa')
