# Generated by Django 4.2.3 on 2023-07-25 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='type',
            field=models.CharField(choices=[('N', 'Новость'), ('A', 'Статья')], default='N', max_length=1),
        ),
    ]
