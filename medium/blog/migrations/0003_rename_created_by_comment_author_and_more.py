# Generated by Django 4.1.2 on 2022-11-05 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_rename_create_by_comment_created_by_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="comment", old_name="created_by", new_name="author",
        ),
        migrations.RenameField(
            model_name="post", old_name="created_by", new_name="author",
        ),
    ]
