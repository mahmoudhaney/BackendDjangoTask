from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from accounts.models import User

class AccountsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='password123', email='test@example.com', phone_number='01150050050')
        self.token = Token.objects.create(user=self.user)

    def test_user_login(self):
        """
        login with correct data
        """
        url = reverse('accounts:login')
        data = {
            'username': 'test_user',
            'password': 'password123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

    def test_user_register(self):
        """
        Register with correct data
        """
        url = reverse('accounts:register')
        data = {
            'username': 'new_user',
            'password': 'new_password',
            'password2': 'new_password',
            'email': 'new@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('token' in response.data)

    def test_user_register_duplicated_username(self):
        """
        Register with duplicated username
        """
        url = reverse('accounts:register')
        data = {
            'username': 'test_user',
            'password': 'new_password',
            'password2': 'new_password',
            'email': 'new@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_register_duplicated_email(self):
        """
        Register with duplicated email
        """
        url = reverse('accounts:register')
        data = {
            'username': 'new_user',
            'password': 'new_password',
            'password2': 'new_password',
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_register_duplicated_phone_number(self):
        """
        Register with duplicated phone_number
        """
        url = reverse('accounts:register')
        data = {
            'username': 'new_user',
            'password': 'new_password',
            'password2': 'new_password',
            'email': 'new@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '01150050050',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('accounts:logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], "You're logged out.")
        self.assertEqual(len(Token.objects.filter(user=self.user)), 0)

    def test_change_password(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('accounts:change-password')
        data = {
            'old_password': 'password123',
            'new_password': 'new_password123',
            'new_password2': 'new_password123',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], "Password changed successfully.")

    def test_change_password_wrong_old_password(self):
        """
        Change Password with wrong old_password
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('accounts:change-password')
        data = {
            'old_password': 'password12',
            'new_password': 'new_password123',
            'new_password2': 'new_password123',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_no_new_password2(self):
        """
        Change Password with no new_password2 provided
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('accounts:change-password')
        data = {
            'old_password': 'password123',
            'new_password': 'new_password123',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
