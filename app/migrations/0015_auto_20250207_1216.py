# Generated by Django 3.2.25 on 2025-02-07 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_rename_email_user_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='Contact',
            new_name='contact',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='Name',
            new_name='name',
        ),
    ]
