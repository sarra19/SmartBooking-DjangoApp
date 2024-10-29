# Generated by Django 4.2 on 2024-10-29 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Person', '0002_person_image_person_location_alter_person_cin'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name': 'Person'},
        ),
        migrations.AddField(
            model_name='person',
            name='face_image',
            field=models.ImageField(blank=True, null=True, upload_to='face_images/'),
        ),
    ]