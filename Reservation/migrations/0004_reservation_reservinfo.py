# Generated by Django 4.2 on 2024-10-29 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reservation', '0003_alter_reservation_passport_numbers'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='reservinfo',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]