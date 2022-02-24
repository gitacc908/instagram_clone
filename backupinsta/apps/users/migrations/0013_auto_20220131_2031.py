# Generated by Django 3.2.6 on 2022-01-31 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20220131_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='comment_like_notification',
            field=models.CharField(blank=True, choices=[(3, 'От людей, на которых вы подписаны'), (2, 'От всех')], default=2, max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='comment_notification',
            field=models.CharField(blank=True, choices=[(1, 'Выкл'), (3, 'От людей, на которых вы подписаны'), (2, 'От всех')], default=2, max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='follow_request_notification',
            field=models.CharField(blank=True, choices=[(1, 'Выкл'), (2, 'От всех')], default=2, max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='like_notification',
            field=models.CharField(blank=True, choices=[(1, 'Выкл'), (3, 'От людей, на которых вы подписаны'), (2, 'От всех')], default=2, max_length=50),
        ),
    ]
