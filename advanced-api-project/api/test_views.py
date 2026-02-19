# api/tests/test_book_api.py

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User, Group
from api.models import Author, Book


class BookAPITestCase(APITestCase):
    """
    Test suite for the Book API.
    Covers CRUD operations, filtering, searching, ordering, and permission checks.
    """

    def setUp(self):
        # --- Create Groups ---
        self.editors_group = Group.objects.create(name='Editors')
        self.admins_group = Group.objects.create(name='Admins')

        # --- Create Users ---
        self.editor_user = User.objects.create_user(username='editor', password='editorpass')
        self.editor_user.groups.add(self.editors_group)

        self.admin_user = User.objects.create_user(username='admin', password='adminpass')
        self.admin_user.groups.add(self.admins_group)

        self.regular_user = User.objects.create_user(username='user', password='userpass')

        # --- Create Authors ---
        self.author1 = Author.objects.create(name='Author One')
        self.author2 = Author.objects.create(name='Author Two')

        # --- Create Books ---
        self.book1 = Book.objects.create(title='Python Basics', publication_year=2020, author=self.author1)
        self.book2 = Book.objects.create(title='Advanced Django', publication_year=2022, author=self.author2)

        # --- API Client ---
        self.client = APIClient()

    # --------------------------
    # Test: List all books
    # --------------------------
    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # --------------------------
    # Test: Retrieve single book
    # --------------------------
    def test_retrieve_book_authenticated(self):
        url = reverse('book-detail', args=[self.book1.id])

        # Unauthenticated → should fail
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticated → should succeed
        self.client.login(username='user', password='userpass')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Python Basics')

    # --------------------------
    # Test: Create a new book
    # --------------------------
    def test_create_book_editor_only(self):
        url = reverse('book-create')
        data = {"title": "New Book", "publication_year": 2023, "author": self.author1.id}

        # Regular user → 403 Forbidden
        self.client.login(username='user', password='userpass')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Editor user → 201 Created
        self.client.login(username='editor', password='editorpass')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['title'], 'New Book')
        self.assertTrue(Book.objects.filter(title='New Book').exists())

    # --------------------------
    # Test: Update a book
    # --------------------------
    def test_update_book_editor_only(self):
        url = reverse('book-update', args=[self.book1.id])
        data = {"title": "Updated Python Basics"}

        # Non-editor → 403 Forbidden
        self.client.login(username='user', password='userpass')
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Editor → 200 OK
        self.client.login(username='editor', password='editorpass')
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Python Basics")

    # --------------------------
    # Test: Delete a book
    # --------------------------
    def test_delete_book_admin_only(self):
        url = reverse('book-delete', args=[self.book1.id])

        # Non-admin → 403 Forbidden
        self.client.login(username='editor', password='editorpass')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Book.objects.filter(id=self.book1.id).exists())

        # Admin → 204 No Content
        self.client.login(username='admin', password='adminpass')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    # --------------------------
    # Test: Filtering
    # --------------------------
    def test_filter_by_author(self):
        url = reverse('book-list')
        response = self.client.get(url, {'author': self.author1.id})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Python Basics')

    def test_filter_by_publication_year_range(self):
        url = reverse('book-list')
        response = self.client.get(url, {'publication_year__gte': 2020, 'publication_year__lte': 2021})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Python Basics')

    # --------------------------
    # Test: Searching
    # --------------------------
    def test_search_title(self):
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Django'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Advanced Django')

    def test_search_author_name(self):
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Author One'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Python Basics')

    # --------------------------
    # Test: Ordering
    # --------------------------
    def test_ordering_publication_year_desc(self):
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': '-publication_year'})
        self.assertEqual(response.data[0]['title'], 'Advanced Django')
        self.assertEqual(response.data[1]['title'], 'Python Basics')
