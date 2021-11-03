from django.shortcuts import render
from apps.users.models import User
from apps.catalog.models import Post



def main(request):

    posts = Post.objects.filter(author__in=request.user.following.all())
    # return render(request, 'registration/password_reset.html')
    return render(request, 'main/index.html', {'posts': posts})
