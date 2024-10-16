# Generated by Django 4.2 on 2024-10-15 20:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Flight', '0003_remove_flight_availability_and_more'),
        ('RentalTransport', '0001_initial'),
        ('Accommodation', '0001_initial'),
        ('Reservation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_reservation', models.CharField(max_length=100)),
                ('special_requests', models.TextField(blank=True, null=True)),
                ('cin', models.PositiveIntegerField()),
                ('phone_number', models.CharField(max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id_accommodation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reservations', to='Accommodation.accommodation')),
                ('id_flight', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reservations', to='Flight.flight')),
                ('id_transport', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reservations', to='RentalTransport.rentaltransport')),
            ],
        ),
        migrations.RemoveField(
            model_name='eventreservation',
            name='event',
        ),
        migrations.RemoveField(
            model_name='flightreservation',
            name='flight',
        ),
        migrations.RemoveField(
            model_name='transportreservation',
            name='rental_transport',
        ),
        migrations.DeleteModel(
            name='AccommodationReservation',
        ),
        migrations.DeleteModel(
            name='EventReservation',
        ),
        migrations.DeleteModel(
            name='FlightReservation',
        ),
        migrations.DeleteModel(
            name='TransportReservation',
        ),
    ]
