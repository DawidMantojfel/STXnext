# Generated by Django 3.1.7 on 2021-03-21 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('STXnext', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='initials',
        ),
    ]
