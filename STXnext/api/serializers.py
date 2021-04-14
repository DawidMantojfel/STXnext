from STXnext.utils import convert_date
from rest_framework import serializers
from STXnext.models import Book, Author


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ['name']


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, required=False)
    published_date = serializers.CharField(required=False)

    class Meta:
        model = Book
        fields = [
            'authors',
            'title',
            'published_date',
            'categories',
            'average_rating',
            'ratings_count',
            'thumbnail',
        ]

    def validate_published_date(self, published_date):
        """

        :param published_date:
        :return: datetime.date object
        takes published date as a string and converts it to datetime.date object
        """
        return convert_date(published_date)

    def create(self, validated_data):
        authors = validated_data.pop('authors', None)
        book, created = Book.objects.get_or_create(**validated_data)
        if authors:
            for author in authors:
                author, _ = Author.objects.get_or_create(name=author['name'])
                author.books.add(book)
        return book

