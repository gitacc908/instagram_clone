from apps.actions.models import Action


def actions_of_following(request):
    actions = None
    if not request.user.is_anonymous:
        actions = Action.objects.exclude(user=request.user)
        following_ids = request.user.following.values_list('id', flat=True)
        if following_ids:
            actions = actions.filter(user_id__in=following_ids)
        actions = actions[:10]
    return {'actions': actions}
