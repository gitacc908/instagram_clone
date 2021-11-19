from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from apps.users.models import User
from apps.catalog.models import Post, Bookmark, Comment
from django.views import View
# from apps.common.forms import PostForm
from apps.catalog.models import Image


def main(request):

    posts = Post.objects.filter(author__in=request.user.following.all())
    return render(request, 'main/index.html', {'posts': posts,})


class LikeView(View):
    def post(self, request, *args, **kwargs):
        post = Post.objects.get(id=request.POST.get('post_id'))
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            return JsonResponse({'status': 'unliked'})
        elif user not in post.likes.all():
            post.likes.add(user)
            return JsonResponse({'status': 'liked'})
        return JsonResponse({'status': 'error'}, status=404)
        

class SaveView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        bookmark, _ = Bookmark.objects.get_or_create(user=user)
        post = Post.objects.get(id=request.POST.get('post_id'))
        if post in bookmark.posts.all():
            bookmark.posts.remove(post)
            return JsonResponse({'status': 'removed'})
        elif post not in bookmark.posts.all():
            bookmark.posts.add(post)
            return JsonResponse({'status': 'saved'})
        return JsonResponse({'status': 'error'}, status=404)


class CommentView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        post_id = request.POST.get('post_id')
        comment = request.POST.get('comment')
        post = get_object_or_404(Post, id=post_id)
        Comment.objects.create(user=user, post=post, text=comment)
        return JsonResponse({'status': 'created'})


class PostView(View):
    def post(self, request, *args, **kwargs):
        post = Post.objects.create(author=request.user)
        post.body = request.POST.get('body')
        post.comments_off = True if request.POST.get('comments_off') == 'true' else False
        post.save()
        for image in request.FILES.getlist('images'):
            Image.objects.create(post=post, image=image)
        return JsonResponse({'status': 'returned'})
