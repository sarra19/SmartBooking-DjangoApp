# Generated by Django 4.2 on 2024-10-29 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Person', '0004_person_keyword'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='face_image',
        ),
    ]
