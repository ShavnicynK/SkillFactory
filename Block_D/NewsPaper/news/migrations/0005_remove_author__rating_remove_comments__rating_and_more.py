# Generated by Django 4.2.3 on 2023-07-25 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_alter_author_rating_rename_rating_author__rating_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='_rating',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='_rating',
        ),
        migrations.RemoveField(
            model_name='post',
            name='_rating',
        ),
        migrations.AddField(
            model_name='author',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comments',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
