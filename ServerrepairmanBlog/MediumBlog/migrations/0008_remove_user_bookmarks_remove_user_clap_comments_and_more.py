# Generated by Django 4.1.3 on 2022-11-07 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MediumBlog', '0007_remove_post_is_published_remove_post_published_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='bookmarks',
        ),
        migrations.RemoveField(
            model_name='user',
            name='clap_comments',
        ),
        migrations.RemoveField(
            model_name='user',
            name='clap_posts',
        ),
        migrations.RemoveField(
            model_name='user',
            name='responded_comments',
        ),
        migrations.RemoveField(
            model_name='user',
            name='responded_posts',
        ),
        migrations.RemoveField(
            model_name='user',
            name='subscribers',
        ),
    ]