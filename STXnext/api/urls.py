from django.urls import path
from .api_views import BooksListAPIView, BookDetailAPIView, BookPostAPIView


urlpatterns = [
    path('GET/books/', BooksListAPIView.as_view(), name='list_of_books'),
    path('GET/books/<int:id>', BookDetailAPIView.as_view(), name='detail'),
    path('POST/books/', BookPostAPIView.as_view(), name='post_books'),
]
