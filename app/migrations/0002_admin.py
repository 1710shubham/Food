# Generated by Django 3.2.25 on 2025-02-05 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Food_Name', models.CharField(max_length=100)),
                ('Food_Description', models.CharField(max_length=100)),
                ('Food_Price', models.CharField(max_length=100)),
                ('Food_category', models.CharField(max_length=100)),
                ('Food_Image', models.CharField(max_length=100)),
            ],
        ),
    ]
