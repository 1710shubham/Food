# Generated by Django 3.2.25 on 2025-02-05 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20250205_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='Food_Image',
            field=models.ImageField(upload_to='app/food_images/'),
        ),
    ]
