# Generated by Django 4.2 on 2024-10-15 20:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Accommodation', '0001_initial'),
        ('Event', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='availability',
        ),
        migrations.AddField(
            model_name='event',
            name='accommodation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='Accommodation.accommodation'),
        ),
    ]
