# from os import replace
from django import template
from apps.users.models import User
from apps.chat.models import Room
# from django.templatetags.static import static
from itertools import chain


register = template.Library()


def get_dm_users(user):
    me = user
    users = User.objects.exclude(id=me.pk)
    dm_users = []
    for user in users:
        for message in user.user_room.room_messages.all():
            if me == message.user:
                dm_users.append(user)
                break
        for message in me.user_room.room_messages.all():
            if user == message.user:
                dm_users.append(user)
                break
    print(dm_users)
    return set(dm_users)

# @register.simple_tag
# def format_current_url_with_lang_code(request, language_code, curren_lang_code):
#     return request.path.replace(curren_lang_code, language_code)


def get_dm_messages(dm_user, me):
    my_messages_sent_to_dm_user = dm_user.user_room.room_messages.filter(
        user=me)
    dm_user_messages_sent_to_me = me.user_room.room_messages.filter(
        user=dm_user)

    result_list = sorted(
        chain(my_messages_sent_to_dm_user, dm_user_messages_sent_to_me),
        key=lambda instance: instance.timestamp
    )
    print(result_list)
    return result_list


register.filter('get_dm_users', get_dm_users)
register.filter('get_dm_messages', get_dm_messages)
