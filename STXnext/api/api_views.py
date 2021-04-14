from django_filters.rest_framework import DjangoFilterBackend
import json
import os
from rest_framework import generics, filters, views
from rest_framework.response import Response
from rest_framework import status
from STXnext.api.serializers import BookSerializer
from STXnext.models import Book


class BookDetailAPIView(generics.RetrieveAPIView):
    """
    retrieve book by id
    """
    lookup_field = 'id'
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BooksListAPIView(generics.ListAPIView):
    """
    list of books from database
    with filtering by date and authors
    and ordering by date
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    filter_fields = ['published_date', 'authors']
    ordering_fields = ['published_date']


class BookPostAPIView(views.APIView):
    """
    POST method only
    allows authenticated user to post books to database
    using google books api or post single or multiple books by himself

    example :
    {
        "authors": [
            {
                "name": "John Ronald Reuel Tolkien"
            }
        ],
        "title": "Hobbit czyli Tam i z powrotem",
        "published_date": "1985-01-01",
        "categories": null,
        "average_rating": null,
        "ratings_count": null,
        "thumbnail": "http://books.google.com/books/content?id=DqLPAAAAMAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api"
    }
    """

    def post(self, request, *args, **kwargs):
        return self.create(request)

    def create(self, request):
        file = r'STXnext/json_books.json'
        with open(file, 'r') as f:
            # checking if file is empty
            empty = os.stat(file).st_size == 0
            if not empty:
                books = json.load(f)
                serializer = BookSerializer(data=books, many=True)
            else:
                serializer = BookSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # flushing content of a file
            open(file, 'w').close()
            return Response({'books': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)





