# Generated by Django 4.2.2 on 2023-08-09 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilephoto',
            name='image',
            field=models.ImageField(default='images/no_profile_image.png', upload_to='media'),
        ),
    ]
