# Generated by Django 4.1.2 on 2022-11-05 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0005_alter_comment_options_alter_post_options"),
    ]

    operations = [
        migrations.AlterModelOptions(name="comment", options={},),
        migrations.AlterModelOptions(name="post", options={},),
        migrations.RenameField(
            model_name="comment", old_name="created_at", new_name="created",
        ),
        migrations.RenameField(
            model_name="post", old_name="created_at", new_name="created",
        ),
    ]