# Generated by Django 3.2.6 on 2021-11-19 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_rename_comments_on_post_comments_off'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='comments_off',
            field=models.BooleanField(default=True, verbose_name='is comments disabled?'),
        ),
    ]