# Generated by Django 3.2 on 2021-04-22 03:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0005_post_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='title',
        ),
    ]