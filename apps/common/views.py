from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render, HttpResponse
from django.views import View
from apps.common.forms import PostForm

from apps.catalog.models import (
    Post, Bookmark, Comment, Image
)
from apps.users.models import User, Contact
from apps.actions.models import Action
import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.actions.utils import create_action


def main(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
    actions = actions[:10]
    posts = Post.objects.filter(author__in=request.user.following.all())
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        print('empty page')
        if request.is_ajax():
        # If the request is AJAX and the page is out of range
        # return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'list_ajax/posts.html', {'posts': posts})
    return render(request, 'main/index.html',{'posts': posts, 'actions': actions})


class LikeView(View):
    def post(self, request, *args, **kwargs):
        post = Post.objects.get(id=request.POST.get('post_id'))
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            return JsonResponse({'status': 'unliked'})
        elif user not in post.likes.all():
            post.likes.add(user)
            create_action(request.user, 'likes', post)
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


class FollowView(View):
    def post(self, request, *args, **kwargs):
        follow_user = get_object_or_404(User, pk=request.POST.get('follow_user_id'))
        if follow_user not in request.user.following.all():
            Contact.objects.create(user_from=request.user, user_to=follow_user)
            create_action(request.user, 'follows', follow_user)
            return JsonResponse({'status': 'followed'})
        else:
            Contact.objects.filter(user_from=request.user, user_to=follow_user).delete()
            return JsonResponse({'status': 'unfollowed'})
