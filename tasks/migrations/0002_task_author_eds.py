# Generated by Django 2.2.4 on 2021-09-27 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_squashed_0114_delete_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='author_eds',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Автор в ЕДС'),
        ),
    ]
