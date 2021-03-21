from rest_framework import serializers
from STXnext.models import Book, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name']


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.StringRelatedField(many=True)

    class Meta:
        model = Book
        fields = [
            #to delete
            'id',
            'authors',
            'title',
            'published_date',
            'categories',
            'average_rating',
            'ratings_count',
            'thumbnail',
        ]



