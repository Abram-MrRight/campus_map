# Generated by Django 4.2.2 on 2023-08-09 20:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('location', '0004_navigation_destination_navigation_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='core.userprofile'),
        ),
        migrations.AlterField(
            model_name='navigation',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='navigations', to='core.userprofile'),
        ),
    ]
