from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from apps.users.models import User
from apps.chat.models import Room


@login_required
def direct(request, user=None):
    if user:
        print(user)
        pass
    common_room, _ = Room.objects.get_or_create(name='common')
    return render(request, 'main/direct.html', {'common_room':common_room})
