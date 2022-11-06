# Generated by Django 4.1.2 on 2022-11-04 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0003_remove_tag_id_alter_tag_content'),
        ('posts', '0005_alter_post_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='tags.tag'),
        ),
        migrations.CreateModel(
            name='TagToPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tags.tag')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]