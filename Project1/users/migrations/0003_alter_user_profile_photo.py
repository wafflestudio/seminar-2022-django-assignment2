# Generated by Django 4.1.2 on 2022-10-23 05:35

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_photo',
            field=models.ImageField(null=True, upload_to=users.models.upload_to),
        ),
    ]
