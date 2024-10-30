# Generated by Django 4.2 on 2024-10-30 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accommodation', '0004_accommodation_feedbacks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accommodation',
            name='price_per_night',
            field=models.DecimalField(decimal_places=0, max_digits=10),
        ),
    ]
