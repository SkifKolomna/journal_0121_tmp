# Generated by Django 2.2.4 on 2021-11-23 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_auto_20211123_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='short_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='Короткое имя'),
        ),
    ]