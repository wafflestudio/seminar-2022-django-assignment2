# Generated by Django 4.1.1 on 2022-11-01 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medium', '0003_alter_comment_cid_alter_post_pid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='cid',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='pid',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]