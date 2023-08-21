# Generated by Django 4.2.2 on 2023-08-09 21:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('location', '0005_alter_location_created_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='navigation',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='navigations', to=settings.AUTH_USER_MODEL),
        ),
    ]
