# Generated by Django 3.2.6 on 2021-11-03 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_auto_20211103_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='posts',
            field=models.ManyToManyField(related_name='bookmarks', to='catalog.Post'),
        ),
    ]
