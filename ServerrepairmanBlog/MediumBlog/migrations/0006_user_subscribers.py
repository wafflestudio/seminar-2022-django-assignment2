# Generated by Django 4.1.3 on 2022-11-06 04:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MediumBlog', '0005_user_is_authorized'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='subscribers',
            field=models.ManyToManyField(related_name='subscribers', to=settings.AUTH_USER_MODEL),
        ),
    ]
