# Generated by Django 3.1.4 on 2021-01-05 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_web', '0002_movie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]
