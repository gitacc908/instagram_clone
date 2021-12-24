from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.views import View
from apps.common.forms import PostForm

from apps.catalog.models import (
    Post, Bookmark, Comment, Image, Tag, CommentReply
)
from apps.users.models import User, Contact
from apps.actions.models import Action
import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.actions.utils import create_action
import redis 
from django.conf import settings
from apps.users.forms import UserAvatarForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# r = redis.Redis(host=settings.REDIS_HOST, 
#                 port=settings.REDIS_PORT, 
#                 db=settings.REDIS_DB)
from django.contrib import messages
from django.utils.translation import ugettext, ugettext_lazy as _
from django.http import HttpResponseRedirect


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    latest_six_posts = Post.objects.filter(author=post.author).exclude(id=post.id)[:6]
    return render(request, 'main/post_detail.html', {'post':post, 'latest_posts':latest_six_posts})


@login_required
def edit_profile(request):
    return render(request, 'main/edit_profile.html')


@login_required
def main(request):
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
    return render(request, 'main/index.html',{'posts': posts})


class LikePostView(LoginRequiredMixin, View):
    login_url = 'signin'

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


class LikeCommentView(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request, *args, **kwargs):
        comment = Comment.objects.get(id=request.POST.get('comment_id'))
        user = request.user
        if user in comment.likes.all():
            comment.likes.remove(user)
            return JsonResponse({'status': 'unliked'})
        elif user not in comment.likes.all():
            comment.likes.add(user)
            return JsonResponse({'status': 'liked'})
        return JsonResponse({'status': 'error'}, status=404)


class SaveView(LoginRequiredMixin, View):
    login_url = 'signin'

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


class CommentView(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request, *args, **kwargs):
        user = request.user
        post_id = request.POST.get('post_id')
        comment = request.POST.get('comment')
        post = get_object_or_404(Post, id=post_id)
        comment = Comment.objects.create(user=user, post=post, text=comment)
        return JsonResponse({'status': 'created', 'comment_id': comment.id})


class CommentReplyView(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=request.POST.get('commentId'))
        CommentReply.objects.create(user=request.user, comment=comment, text=request.POST.get('replyText'))
        return JsonResponse({'status': 'created'})


class PostView(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request=request)
        if form.is_valid():
            post = form.save(commit=False)
            tags = form.cleaned_data.get('tag')
            for tag in tags:
                tag, _ = Tag.objects.get_or_create(name=tag)
                post.tags.add(tag)
            Image.objects.bulk_create([
                Image(post=form.instance, image=image) for image in request.FILES.getlist('images')
            ])
            post.save()    
            return JsonResponse({'status': 'created'})
        error_dict = {'status': 'form_invalid', 'form_errors': form.errors}
        return HttpResponse(json.dumps(error_dict),content_type="application/json", status=400)


class FollowView(LoginRequiredMixin, View):
    login_url = 'signin'

    def post(self, request, *args, **kwargs):
        follow_user = get_object_or_404(User, pk=request.POST.get('follow_user_id'))
        if follow_user not in request.user.following.all():
            Contact.objects.create(user_from=request.user, user_to=follow_user)
            create_action(request.user, 'follows', follow_user)
            return JsonResponse({'status': 'followed'})
        else:
            Contact.objects.filter(user_from=request.user, user_to=follow_user).delete()
            return JsonResponse({'status': 'unfollowed'})


class UpdateAvatarView(LoginRequiredMixin, View):
    login_url = 'signin'
    
    def post(self, request, *args, **kwargs):
        form = UserAvatarForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'avatar updated!'}, status=200)
        return JsonResponse({'status':'error'}, status=424)


class UnfollowView(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        Contact.objects.filter(user_from=request.user, user_to=user).delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class DeletePost(LoginRequiredMixin, View):
    login_url = 'signin'

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        post.delete()
        # messages.success(request, _('Your post has been deleted'))
        return redirect(request.user.get_absolute_url())
