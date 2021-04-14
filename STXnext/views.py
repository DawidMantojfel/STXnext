from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse as reverse_url
from django.http import HttpResponse
import json
from .models import Book, Author
import os
import requests
from rest_framework import status


def home_page(request):
    context = {}
    FILE = 'STXnext/json_books.json'
    ids = Book.objects.order_by('id')
    if len(ids) > 0:
        id_first = ids[0].id
        last = ids.reverse()[0].id
        context['count_books'] = [id for id in range(id_first,last+1)]
        # flush database if there is more than 200 records
        if last - id_first > 200:
            Book.objects.all().delete()
            Author.objects.all().delete()
            messages.warning(request, "More than 200 records. Database reset")
            return redirect(reverse_url('home'))
    not_empty = os.stat(FILE).st_size != 0
    context['not_empty'] = not_empty
    return render(request, 'STXnext/home_page.html', context)


def save_to_file(request):
    query = request.GET.get('query')
    FILE = 'STXnext/json_books.json'
    URL = f'https://www.googleapis.com/books/v1/volumes?q={query}'
    books = get_from_google_api(URL)
    with open(FILE, 'w') as f:
        f.write(json.dumps(books, indent=4))
        messages.success(
            request,
            f"books with query{query} added to file ",
            fail_silently=True
                        )
    return redirect(reverse_url('home'))


def get_from_google_api(url):
    response = requests.request("GET", url)
    json_response = response.json()
    books = []
    book = {}
    if response.status_code == 200:
        if json_response.get('items'):
            for result in json_response['items']:
                authors = result['volumeInfo'].get('authors')
                if authors:
                    book['authors'] = []
                    for author in authors:
                        book['authors'].append({'name': author})
                book['title'] = result['volumeInfo'].get('title')
                book['published_date'] = result['volumeInfo'].get('publishedDate')
                categories = result['volumeInfo'].get('categories')
                book['categories'] = ', '.join(categories) if categories else None
                book['average_rating'] = result['volumeInfo'].get('average_rating')
                book['ratings_count'] = result['volumeInfo'].get('ratings_count')
                book['thumbnail'] = result['volumeInfo']['imageLinks'].get('thumbnail') \
                    if result['volumeInfo'].get('imageLinks') else None
                books.append(book)
                book = {}
            return books
        return HttpResponse(f'no books found {status.HTTP_204_NO_CONTENT}')
    return HttpResponse(f'got wrong response from google {response.status_code}')












