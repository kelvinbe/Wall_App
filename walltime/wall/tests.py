from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test  import APITestCase
from wall.models import Message
from django.urls import reverse


# class MessageTests(APITestCase):
#     def test_create_message(self):
#         """
#         Ensure we can create a new message.
#         """
#         url = '/message/'
#         data = {'message': 'Hello', 'author': 'beno', 'title': 'Testing Testing'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Message.objects.count(), 1)
#         self.assertEqual(Message.objects.get().message, 'Hello')

class RegistrationTest(APITestCase):
    def test_registration(self):
        """
        Ensure we can create a new message.
        """
        url = '/register/'
        data = {'username': 'tester','email': 'k@gmail.com', 'password': 'beno', 'confirm_password': 'beno'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    class LogInTest(APITestCase):
        def setUp(self):
            self.credentials = {
                'username': 'testuser',
                'password': 'secret'}
            User.objects.create_user(**self.credentials)
            self.token = Token.objects.create(user=self.credentials)
        def test_login(self):
            # send login data
            response = self.client.post('/login/', self.credentials)
            # should be logged in now
            self.assertTrue(response.context['user'].is_authenticated)
