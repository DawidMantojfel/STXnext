from rest_framework import status
from rest_framework.response import Response
from STXnext.models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from rest_framework import generics, viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from STXnext.views import save_books_to_file


class BookDetailAPIView(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BooksListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    filter_fields = ['published_date', 'authors']
    ordering_fields = ['published_date']


# class UpdateAPIView(generics.ListCreateAPIView):
#
#     serializer_class = BookSerializer(many=True)
#     filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
#     filter_fields = ['published_date', 'authors']
#     ordering_fields = ['published_date']
#
#     def get_queryset(self):
#         save_books(self.request, 'war')
#         queryset = Book.objects.all()
#         return queryset






