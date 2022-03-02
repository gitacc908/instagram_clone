from aiohttp import request
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.views import View
from apps.common.forms import PostForm, UserForm, UserNotificationForm, StoryForm

from apps.catalog.models import (
    Post, Bookmark, Comment, Image, Tag, CommentReply, Story
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
from apps.users.get_country import get_location
from django.views.generic import UpdateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Q


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    latest_six_posts = Post.objects.filter(author=post.author).exclude(id=post.id)[:6]
    return render(request, 'main/post_detail.html', {'post':post, 'latest_posts':latest_six_posts})


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'profile/edit_profile.html'
    success_url = reverse_lazy('edit_profile')

    def get_success_url(self):
        return reverse('edit_profile',  kwargs={'pk':
                                                     self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(EditProfileView, self).get_context_data(**kwargs)
        context['password_form'] = PasswordChangeForm(self.request.user)
        context['notification_form'] = UserNotificationForm(instance=self.request.user)
        device, device_full, c = get_location(self.request)
        context['country'] = c.name
        context['device'] = device
        context['device_full'] = device_full
        return context


@login_required
def edit_password_view(request):
    form = UserForm(instance=request.user)
    notification_form = UserNotificationForm(instance=request.user)
    password_form = PasswordChangeForm(request.user)
    device, device_full, c = get_location(request)

    if request.method == 'POST':
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            password_form.save()
            return redirect('edit_profile', request.user.pk)
    return render(request, 'profile/edit_profile.html', {'form':form, 'password_form': password_form, 
                                                        'notification_form': notification_form,
                                                        'device': device, 'device_full': device_full,
                                                        'country': c.name})


@login_required
def edit_notification_view(request):
    form = UserForm(instance=request.user)
    notification_form = UserNotificationForm(instance=request.user)
    password_form = PasswordChangeForm(request.user)
    device, device_full, c = get_location(request)

    if request.method == 'POST':
        notification_form = UserNotificationForm(request.POST)
        if notification_form.is_valid():
            notification_form.save()
            return redirect('edit_profile', request.user.pk)
    return render(request, 'profile/edit_profile.html', {'form':form, 'password_form': password_form, 
                                                        'notification_form': notification_form,
                                                        'device': device, 'device_full': device_full,
                                                        'country': c.name})


@login_required
def search(request):
    query = request.GET.get('q')
    mobile = request.GET.get('mobile')
    desktop = request.GET.get('desktop')
    hashtag = request.GET.get('hashtag')
    tag = request.GET.get('tag')
    
    if tag:
        tag = get_object_or_404(Tag, name=tag)
        posts = Post.objects.filter(tags__in=[tag,])
        return render(request, 'main/search.html', {'posts': posts})

    if query and request.is_ajax():
        if hashtag:
            tags = Tag.objects.filter(name__icontains=query)
            if mobile:
                html = render_to_string(
                template_name="search/result_mobile.html", 
                context={"tags": tags}
            )
            elif desktop:
                html = render_to_string(
                template_name="search/result_desktop.html", 
                context={"tags": tags}
            )
        else:
            users = User.objects.filter(
                Q(username__icontains=query)
                | Q(full_name__icontains=query)
            )
            if mobile:
                html = render_to_string(
                template_name="search/result_mobile.html", 
                context={"users": users}
            )
            elif desktop:
                html = render_to_string(
                template_name="search/result_desktop.html", 
                context={"users": users}
            )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)
    following_ids = list(request.user.following.values_list('id', flat=True))
    following_ids.append(request.user.id)
    posts = Post.objects.exclude(author_id__in=following_ids)
    return render(request, 'main/search.html', {'posts': posts})


@login_required
def main(request):
    my_following = request.user.following.all()
    stories = Story.objects.filter(user__in=my_following)
    posts = Post.objects.filter(author__in=my_following)
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
        # If the request is AJAX and the page is out of range
        # return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'list_ajax/posts.html', {'posts': posts})
    return render(request, 'main/index.html',{'posts': posts, 'stories': stories})


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
        print(request.POST, request.FILES)
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


class StoryPostView(LoginRequiredMixin, View):
    login_url = 'signin'
    form = StoryForm

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST, request.FILES, request=request)
        if form.is_valid():
            form.save()
            return JsonResponse({'status':'success'}, status=201)
        return JsonResponse({'status':form.errors}, status=424)
