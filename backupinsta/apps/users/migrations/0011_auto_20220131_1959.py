# Generated by Django 3.2.6 on 2022-01-31 19:59

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_user_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='comment_like_notification',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(3, 'От людей, на которых вы подписаны'), (2, 'От всех')], default=2, max_length=3),
        ),
        migrations.AddField(
            model_name='user',
            name='comment_notification',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Выкл'), (3, 'От людей, на которых вы подписаны'), (2, 'От всех')], default=2, max_length=5),
        ),
        migrations.AddField(
            model_name='user',
            name='follow_request_notification',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Выкл'), (2, 'От всех')], default=2, max_length=3),
        ),
        migrations.AddField(
            model_name='user',
            name='like_notification',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Выкл'), (3, 'От людей, на которых вы подписаны'), (2, 'От всех')], default=2, max_length=5),
        ),
    ]
