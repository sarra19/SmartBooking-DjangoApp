# Generated by Django 4.2 on 2024-10-16 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Flight', '0004_flight_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flight',
            name='image',
        ),
    ]
