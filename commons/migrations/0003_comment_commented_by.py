# Generated by Django 2.2.4 on 2021-08-18 10:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('commons', '0002_auto_20210818_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='commented_by',
            field=models.ForeignKey(blank=True, max_length=100, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comment_commented_by', to=settings.AUTH_USER_MODEL, verbose_name='Создана'),
        ),
    ]
