# Generated by Django 4.1.6 on 2024-10-19 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0003_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='image',
            new_name='image_file',
        ),
    ]
