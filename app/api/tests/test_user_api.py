from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

SIGNUP_USER_URL = reverse('api:signup')
LOGIN_URL = reverse('api:login')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    '''Test API (public)'''

    def setUp(self):
        self.client = APIClient()

    def test_signup_valid_user_success(self):
        '''Test creating user with valid payload is successful'''
        payload = {
            'email': 'a.collins@todo.net',
            'password': '@TEi2^9OuvS',
            'name': 'Arthur Collins'
        }
        res = self.client.post(SIGNUP_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_exists(self):
        '''Test creating a user that already exists fails'''
        payload = {
            'email': 'a.collins@todo.net',
            'password': 'CeSar$5673',
            'name': 'Alex Collins',
        }
        create_user(**payload)

        res = self.client.post(SIGNUP_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        '''Test that the password must be more than 8 characters'''
        payload = {
            'email': 'a.collins@todo.net',
            'password': 'psw',
            'name': 'Arthur Collins',
        }
        res = self.client.post(SIGNUP_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_login_user(self):
        '''Test that JWT  is created for the user'''
        payload = {'email': 'a.collins@todo.net', 'password': '@TEi2^9OuvS'}
        create_user(**payload)
        res = self.client.post(LOGIN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_login_user_invalid_credentials(self):
        '''Test that JWT is not created if invalid credentials are given'''
        create_user(email='bigseller@gmail.com', password="56842Luis1984")
        payload = {'email': 'bigseller@gmail.com', 'password': 'wrong'}
        res = self.client.post(LOGIN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_no_user(self):
        '''Test that JWT is not created if user doesn't exist'''
        payload = {'email': 'tanyablack@gmail.com', 'password': 'H29BrUr43E'}
        res = self.client.post(LOGIN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_missing_field(self):
        '''Test that email and password are required'''
        res = self.client.post(LOGIN_URL, {'email': 'a.collins@todo.net',
                                           'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
