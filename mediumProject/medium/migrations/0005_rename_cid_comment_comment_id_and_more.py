# Generated by Django 4.1.1 on 2022-11-03 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medium', '0004_alter_comment_cid_alter_post_pid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='cid',
            new_name='comment_id',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='pid',
            new_name='post_id',
        ),
    ]