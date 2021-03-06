from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=1000)
    published_date = models.DateField(auto_now_add=False, null=True)
    categories = models.CharField(max_length=300, null=True, blank=True)
    average_rating = models.FloatField(null=True, blank=True)
    ratings_count = models.IntegerField(null=True, blank=True)
    thumbnail = models.URLField(null=True, blank=True)

    def __str__(self):
        return f'title: {self.title} \n' \
               f'date of publication: {self.published_date} \n' \
               f'authors: {[author.name for author in self.authors.all()]}'


class Author(models.Model):
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(Book, related_name='authors')

    def __str__(self):
        return str(self.name)


