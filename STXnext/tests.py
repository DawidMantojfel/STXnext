import os

from django.test import TestCase
from .models import Book, Author
from .views import save_to_file
import datetime
from .utils import convert_date, convert_initials
import requests
from django.test.client import RequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class BooksListAPIViewTest(APITestCase):

    BOOKS_LIST_URL = reverse('list_of_books')
    POST_BOOKS = reverse('post_books')

    def setUp(self) -> None:
        today = datetime.date.today()
        hobbit = Book.objects.create(title='Hobbit',
                                     published_date=today,
                                     categories=['fantasy'],
                                     average_rating=4.5,
                                     ratings_count=100,
                                     thumbnail='http://books.google.com/books/content?id=YyXoAAAACAAJ'
                                               '&printsec=frontcover&img=1&zoom=1&source=gbs_api')
        war = Book.objects.create(title='war',
                                  published_date=today,
                                  categories=['history'],
                                  average_rating=4,
                                  ratings_count=10,
                                  thumbnail="http://books.google.com/books/content?id=sqRHAQAAMAAJ"
                                           "&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api")

        books = [war, hobbit]

    def test_response_ok(self):
        response = self.client.get(self.BOOKS_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_of_api_books(self):
        response = self.client.get(self.BOOKS_LIST_URL)
        self.assertEqual(len(response.data), 2)

    def test_detail_book(self):
        hobbit = Book.objects.get(title='Hobbit')
        response = self.client.get('/GET/books/'+str(hobbit.id))
        title = response.data['title']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(title, 'Hobbit')

    def test_posting_books(self):
        response = self.client.get(self.POST_BOOKS)
        # CHECK IF WE POSTED BOOKS AFTER HITTING GIVEN API URL
        self.assertGreater(len(response.data), 2)


class ViewTests(TestCase):
    SAVE_TO_FILE_URL = reverse('save_books_to_file')

    def setUp(self):
        """RequestFactory kreuje dummy request"""
        self.factory = RequestFactory()

    def test_save_to_file(self):
        data = [self]
        file = 'STXnext/json_books.json'
        request = self.factory.get(self.SAVE_TO_FILE_URL)
        request.data = {'query': 'hobbit'}
        self.assertNotEqual(os.stat(file).st_size,0)




class BookModelTests(TestCase):

    def setUp(self) -> None:
        today = datetime.date.today()
        date_in_past = datetime.datetime.strptime('1980 12 12', "%Y %m %d")
        tolkien = Author.objects.create(name='John Ronald Reuel Tolkien')
        charles = Author.objects.create(name="Charles Dixon")
        hobbit = Book.objects.create(title='Hobbit',
                                     published_date=today,
                                     categories=['fantasy'],
                                     average_rating=4.5,
                                     ratings_count=100,
                                     thumbnail='http://books.google.com/books/content?id=YyXoAAAACAAJ'
                                               '&printsec=frontcover&img=1&zoom=1&source=gbs_api')

        war = Book.objects.create(title='war',
                                  published_date=date_in_past,
                                  categories=['history'],
                                  average_rating=4,
                                  ratings_count=10,
                                  thumbnail="http://books.google.com/books/content?id=sqRHAQAAMAAJ"
                                           "&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api")
        tolkien.books.add(hobbit)
        charles.books.add(hobbit)

    def test_books_ids(self):
        ids = Book.objects.order_by('id')
        if len(ids) > 0:
            id_first = ids[0].id
            last = ids.reverse()[0].id
            self.assertEqual(last-id_first,1)
        else:
            self.assertEqual(len(ids), 0)

    def test_books_exists(self):
        books_count = Book.objects.all().count()
        book_exists = Book.objects.filter(title='Hobbit').exists()
        self.assertEqual(books_count, 2)
        self.assertNotEqual(books_count, 0)
        self.assertTrue(book_exists)

    def test_book_have_two_authors(self):
        hobbit = Book.objects.get(title='Hobbit')
        authors = hobbit.authors.all().count()
        self.assertEqual(authors, 2)
        self.assertNotEqual(authors, 1)


class AuthorModelTests(TestCase):

    def setUp(self) -> None:
        hobbit = Book.objects.create(title='Hobbit',
                                     published_date=datetime.date.today(),
                                     categories=['fantasy'],
                                     average_rating=4.5,
                                     ratings_count=100,
                                     thumbnail='http://books.google.com/books/content?id=YyXoAAAACAAJ'
                                               '&printsec=frontcover&img=1&zoom=1&source=gbs_api')

        hobbit2 = Book.objects.create(title='"The Hobbit and Philosophy"',
                                      published_date=datetime.date.today(),
                                      categories=['fantasy'],
                                      average_rating=4.5,
                                      ratings_count=100,
                                      thumbnail="http://books.google.com/books/content?id=33HUiYwuBxQC"
                                                "&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api")

        tolkien = Author.objects.create(name='John Ronald Reuel Tolkien')
        tolkien.books.add(hobbit)
        tolkien.books.add(hobbit2)

    def test_author_has_two_books(self):
        tolkien = Author.objects.get(name='John Ronald Reuel Tolkien')
        number_of_books = tolkien.books.all().count()
        self.assertEqual(number_of_books, 2)
        self.assertNotEqual(number_of_books, 1)


class HelperFunctionsTests(TestCase):

    def test_convert_date_function(self):
        ymd = datetime.datetime.strptime('2012 02 15', "%Y %m %d")
        ymd_converted = convert_date("2012-02-15")
        ym = datetime.datetime.strptime('2012 02', "%Y %m")
        ym_converted = convert_date("2012-02")
        y = datetime.datetime.strptime('2012', "%Y")
        y_converted = convert_date("2012")
        self.assertEqual(ymd_converted, ymd)
        self.assertEqual(ym_converted, ym)
        self.assertEqual(y_converted, y)
        self.assertIsNone(convert_date(None))


