# Generated by Django 4.1.2 on 2022-11-05 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_rename_created_by_comment_author_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(name="comment", options={},),
        migrations.AlterModelOptions(name="post", options={},),
    ]