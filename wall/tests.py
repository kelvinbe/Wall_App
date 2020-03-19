from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
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
        client = APIClient()
        response = self.client.post('/register', {'username': 'kev', 'password': 'lala', 'email': 'll@gmail.com'}, format='json')
        self.assertEqual(response.status_code, 200)


class LogInTest(APITestCase):
     def login(self):
         new_user1_data = {
            "username": "dummy",
            "first_name": "a",
            "last_name": "dummy",
            "password": "randompassword",
            "email": "test@test.com",
            }

         new_user1 = User.objects.create_user(
            username=new_user1_data["username"],
            first_name=new_user1_data["first_name"],
            last_name=new_user1_data["last_name"],
            email=new_user1_data["email"],
            password=new_user1_data["password"]
            )
         self.new_user = User.objects.create(user=new_user1)

         response = self.client.post('/login', {'username': 'dummy', 'password': 'randompassword'}, format='json')
         self.assertEqual(response.status_code, 200)