import requests
from django.shortcuts import render, redirect
from STXnext.models import Book, Author
from .utils import convert_date
from django.contrib import messages


def home_page(request):
    context = {}
    count_books = Book.objects.all().count()
    if count_books > 0:
        id_first = Book.objects.first().id
        context['count_books'] = [id for id in range(id_first,id_first+count_books)]
    return render(request, 'STXnext/home_page.html', context)


def save_books(request, query='Hobbit'):
    url = f'https://www.googleapis.com/books/v1/volumes?q={query}'
    response = requests.request("GET", url).json()
    for result in response['items']:
        book_info = result['volumeInfo']
        title = book_info.get('title')
        published_date = convert_date(book_info.get('publishedDate'))
        categories = book_info.get('categories')
        average_rating = book_info.get('averageRating')
        ratings_count = book_info.get('ratingsCount')
        thumbnail = book_info['imageLinks'].get('thumbnail') if book_info.get('imageLinks') else None
        book_authors = book_info.get('authors')
        book, created = Book.objects.get_or_create(title=title,
                                                   published_date=published_date,
                                                   categories=categories,
                                                   average_rating=average_rating,
                                                   ratings_count=ratings_count,
                                                   thumbnail=thumbnail)
        if created:
            book.save()
            if book_authors:
                for author_name in book_authors:
                    author = Author(name=author_name)
                    author.name_initials()
                    author, p = Author.objects.get_or_create(name=author)
                    author.books.add(book)
                messages.success(request, f"Book '{book.title}' by {book_authors} added to database ",fail_silently=True)
        else:
            messages.warning(request, f' "{book.title}"by {" and ".join(book_authors)} is already in the database',fail_silently=True)
    return redirect('home')







