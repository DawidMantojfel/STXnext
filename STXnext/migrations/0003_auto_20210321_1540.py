# Generated by Django 3.1.7 on 2021-03-21 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('STXnext', '0002_remove_author_initials'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ('published_date',)},
        ),
    ]
