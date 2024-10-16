# Generated by Django 4.2 on 2024-10-14 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_name', models.CharField(max_length=100)),
                ('flight_number', models.CharField(max_length=20)),
                ('departure_city', models.CharField(max_length=100)),
                ('arrival_city', models.CharField(max_length=100)),
                ('departure_date', models.DateTimeField()),
                ('arrival_date', models.DateTimeField()),
                ('airline', models.CharField(max_length=100)),
                ('price_per_place', models.DecimalField(decimal_places=2, max_digits=10)),
                ('available_places', models.PositiveIntegerField()),
                ('availability', models.BooleanField(default=True)),
            ],
        ),
    ]
