from django.http.response import JsonResponse
from django.shortcuts import render
from apps.users.models import User
from apps.catalog.models import Post
from django.views import View


def main(request):

    posts = Post.objects.filter(author__in=request.user.following.all())
    return render(request, 'main/index.html', {'posts': posts})


class LikeView(View):
    def post(self, request, *args, **kwargs):
        post = Post.objects.get(id=request.POST['id'])
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            return JsonResponse({'status': 'unliked'})
        elif user not in post.likes.all():
            post.likes.add(user)
            return JsonResponse({'status': 'liked'})
        return JsonResponse({'status': 'error'}, status=404)
        
