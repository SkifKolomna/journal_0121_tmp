# Generated by Django 2.2.4 on 2021-11-23 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_auto_20211123_1320'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='location',
            new_name='full_name',
        ),
    ]
