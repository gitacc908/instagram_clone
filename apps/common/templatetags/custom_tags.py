from django import template
from apps.users.models import User


register = template.Library()


def get_liked_users(following, likes):
    return set(following).intersection(set(likes))

def get_first_user(liked_users):
    return list(liked_users)[0]

def follow_suggestion(user):
    # if user.following.all():
    #     following_users = user.following.all()
    # following_of_following = [user.following.all() for user in following_users]


    exclude_list = [user.pk for user in user.following.all()]
    exclude_list.append(user.pk)
    if user.following.count() > 0:
        suggestions = User.objects.filter(is_active=True)\
            .exclude(id__in=exclude_list)
    else:
        suggestions = User.objects.filter(is_active=True)\
            .exclude(id=user.pk)
    return suggestions


register.filter('get_liked_users', get_liked_users)
register.filter('get_first_user', get_first_user)
register.filter('follow_suggestion', follow_suggestion)
