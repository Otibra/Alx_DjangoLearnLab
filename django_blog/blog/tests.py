from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class UserAuthTests(TestCase):
    def test_registration_and_login(self):
        # Register a new user
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123'
        })
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='testuser').exists())

        # Login with correct credentials
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'StrongPass123'
        })
        self.assertRedirects(response, reverse('profile'))

    def test_profile_editing(self):
        user = User.objects.create_user(username='testuser2', password='StrongPass123')
        self.client.login(username='testuser2', password='StrongPass123')

        # Update email
        response = self.client.post(reverse('profile'), {
            'username': 'testuser2',
            'email': 'newemail@example.com'
        })
        self.assertRedirects(response, reverse('profile'))
        user.refresh_from_db()
        self.assertEqual(user.email, 'newemail@example.com')
        