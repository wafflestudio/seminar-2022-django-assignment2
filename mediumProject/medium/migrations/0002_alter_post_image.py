# Generated by Django 4.1.1 on 2022-10-31 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medium', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='post/'),
        ),
    ]