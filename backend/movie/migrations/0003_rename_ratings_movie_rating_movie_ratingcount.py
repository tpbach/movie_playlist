# Generated by Django 4.0.3 on 2022-03-08 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='ratings',
            new_name='rating',
        ),
        migrations.AddField(
            model_name='movie',
            name='ratingCount',
            field=models.IntegerField(default=0),
        ),
    ]
