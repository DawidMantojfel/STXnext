from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import BooksListAPIView, BookDetailAPIView
#
# router = DefaultRouter()
# router.register(r'post', DeleteBooksAPIVIew, basename='post')

urlpatterns = [
    path('GET/books/', BooksListAPIView.as_view(), name='list_of_books'),
    path('GET/books/<int:id>', BookDetailAPIView.as_view(), name='detail'),
]