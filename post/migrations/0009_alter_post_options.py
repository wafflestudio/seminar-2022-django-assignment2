# Generated by Django 4.1.2 on 2022-10-11 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0008_alter_comment_post'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_at']},
        ),
    ]