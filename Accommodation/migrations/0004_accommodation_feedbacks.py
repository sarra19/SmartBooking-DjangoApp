# Generated by Django 5.1.2 on 2024-10-29 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Accommodation", "0003_accommodation_ratings"),
    ]

    operations = [
        migrations.AddField(
            model_name="accommodation",
            name="feedbacks",
            field=models.JSONField(default=list),
        ),
    ]
