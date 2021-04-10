import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from STXnext.models import Book, Author
from .utils import convert_date
from django.contrib import messages
from STXnext.settings import BASE_DIR
import os
import json


def home_page(request):
    context = {}
    ids = Book.objects.order_by('id')
    if len(ids) > 0:
        id_first = ids[0].id
        last = ids.reverse()[0].id
        context['count_books'] = [id for id in range(id_first,last+1)]
    return render(request, 'STXnext/home_page.html', context)

def save_books_to_file(request):
    FILE = 'json_books.json'
    if request.method == "POST":
        query = request.POST.get('query')
        URL = f'https://www.googleapis.com/books/v1/volumes?q={query}'
        response = requests.request("GET", URL)
        response = response.json()
        books = []
        book = {}
        for result in response['items']:
            book['title'] = result['volumeInfo'].get('title')
            book['authors'] = result['volumeInfo'].get('authors')
            book['published_date'] = result['volumeInfo'].get('publishedDate')
            book['categories'] = result['volumeInfo'].get('categories')
            book['average_rating'] = result['volumeInfo'].get('average_rating')
            book['ratings_count'] = result['volumeInfo'].get('ratings_count')
            book['thumbnail'] = result['volumeInfo']['imageLinks'].get('thumbnail') if result['volumeInfo'].get('imageLinks') else None
            books.append(book)
            book = {}
        with open((os.path.join(BASE_DIR, FILE)), 'w') as f:
            f.write(json.dumps(books, indent=4))
        return save_books_to_database(request, FILE)

def save_books_to_database(request, file):
    with open(file, 'r') as f:
        books = json.loads(f.read())
        for json_book in books:
            book, created = Book.objects.get_or_create(title=json_book['title'],
                                                       published_date=convert_date(json_book['published_date']),
                                                       categories=json_book['categories'],
                                                       average_rating=json_book['average_rating'],
                                                       ratings_count=json_book['ratings_count'],
                                                       thumbnail=json_book['thumbnail'])
            if created:
                book.save()
                if json_book['authors']:
                    for author_name in json_book['authors']:
                        author, _ = Author.objects.get_or_create(name=author_name)
                        author.books.add(book)
                    messages.success(request, f"Book '{json_book['title']}' by {json_book['authors']} added to database ",
                                     fail_silently=True)
            else:
                messages.warning(request, f"Book '{json_book['title']}' by {json_book['authors']} is already in the database",
                                 fail_silently=True)
    return redirect('home')







