# Generated by Django 4.2 on 2024-10-29 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Person', '0005_remove_person_face_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='keyword',
            field=models.CharField(default=' ', max_length=10),
        ),
    ]