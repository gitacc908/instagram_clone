# Generated by Django 3.2.6 on 2022-03-01 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20220131_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='like_notification',
            field=models.CharField(blank=True, choices=[(1, 'Выкл'), (3, 'От людей, на которых вы подписаны'), (2, 'От всех')], default=2, max_length=50, verbose_name='like notif'),
        ),
    ]
