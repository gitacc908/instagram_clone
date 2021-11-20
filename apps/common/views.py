from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render, HttpResponse
from apps.catalog.models import Post, Bookmark, Comment
from django.views import View
from apps.common.forms import PostForm
from apps.catalog.models import Image
import json


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
        form = PostForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            Image.objects.bulk_create([
                Image(post=form.instance, image=image) for image in request.FILES.getlist('images')
            ])
            return JsonResponse({'status': 'created'})
        error_dict = {'status': 'form_invalid', 'form_errors': form.errors}
        return HttpResponse(json.dumps(error_dict),content_type="application/json", status=400)
