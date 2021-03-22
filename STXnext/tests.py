from django.test import TestCase
from .models import Book, Author
import datetime
from .utils import convert_date, convert_initials
import requests
from .views import save_books
from django.test.client import RequestFactory


class ViewTests(TestCase):

    def setUp(self):
        """RequestFactory kreuje dummy request"""
        self.factory = RequestFactory()

    def test_save_books(self):
        url = 'https://www.googleapis.com/books/v1/volumes?q=Hobbit'
        request = self.factory.get(path='/save/')
        response = requests.request("GET", url).json()
        num_of_books_from_response = len(response['items'])
        save_books(request)
        num_books_from_database = Book.objects.all().count()
        self.assertEqual(num_books_from_database, num_of_books_from_response)


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

    def test_author_name_was_converted_to_initials(self):
        tolkien = Author(name='John Ronald Reuel Tolkien')
        tolkien.name_initials()
        self.assertEqual(tolkien.name, 'J. R. R. Tolkien')


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

    def test_convert_initials_function(self):
        full_name = 'Corey Olsen'
        converted = convert_initials(full_name)
        self.assertEqual(converted, 'C. Olsen')

