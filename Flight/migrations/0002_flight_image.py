# Generated by Django 4.2 on 2024-10-14 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Flight', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='flight_images/'),
        ),
    ]
