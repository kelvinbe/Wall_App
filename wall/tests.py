from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from wall.models import Message


class MessageTests(APITestCase):
    def setUp(self):
        self.username = 'john_doe'
        self.password = 'foobar'
        self.user = User.objects.create(
            username=self.username, password=self.password)
        self.client.force_authenticate(user=self.user)

    def test_message(self):
        response = self.client.post(
            '/message/', {'title': 'Foo Bar', 'description': 'olaaa'}, format='json')
        self.assertEqual(response.status_code, 201)


class RegistrationTest(APITestCase):
    def test_registration(self):
        client = APIClient()
        response = self.client.post(
            '/register', {'username': 'kev', 'password': 'lala', 'email': 'll@gmail.com'}, format='json')
        self.assertEqual(response.status_code, 200)


class LoginTests(APITestCase):
    def login(self):
        client = APIClient()
        new_user1_data = {
            "username": "kev",
            "password": "lala",
            "email": "ll@gmail.com"
        }
        new_user1 = User.objects.create_user(
            username=new_user1_data["username"],
            email=new_user1_data["email"],
            password=new_user1_data["password"]
        )
        self.new_user = User.objects.create(user=new_user1)
        client.login(username='kev', password='lala')
