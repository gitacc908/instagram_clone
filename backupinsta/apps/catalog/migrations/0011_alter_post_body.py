# Generated by Django 3.2.6 on 2021-11-20 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_alter_post_comments_off'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=models.TextField(null=True, verbose_name='description of post'),
        ),
    ]
