# Generated by Django 4.0.3 on 2023-05-05 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_favourites_vidfav'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favourites',
            name='vidfav',
        ),
        migrations.RemoveField(
            model_name='favourites',
            name='favourite',
        ),
        migrations.AddField(
            model_name='favourites',
            name='favourite',
            field=models.ManyToManyField(blank=True, related_name='vaooo', to='app.uploadworkoutvideo'),
        ),
    ]
