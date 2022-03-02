from django import forms
from apps.catalog.models import Post, Tag, Story
from apps.catalog.validators import validate_tag
from apps.users.models import User
from apps.users.choices import *


class PostForm(forms.ModelForm):
    tag = forms.CharField(max_length=30, required=False)

    class Meta:
        model = Post
        fields = ('body', 'comments_off', 'tag')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PostForm, self).__init__(*args, **kwargs)

    def clean_tag(self):
        # validate if body contains tags to create or get
        body = self.cleaned_data.get('body')
        tags = [word for word in body.split(' ') if word.startswith('#')]
        hashtags = []
        # filter(validate_tag, tags)
        # hashtags.extend(tags)
        for tag in tags:
            # tag = Tag(name=tag)
            # if object is valid
            validate_tag(tag)
            # if not tag.full_clean():
            hashtags.append(tag)
        return hashtags

    def save(self, commit=True):
        post = super(PostForm, self).save(commit=False)
        post.author = self.request.user
        post.comments_off = True if self.cleaned_data.get(
            'comments_off') == 'true' else False
        body = self.cleaned_data.get('body')
        post.body = " ".join(filter(lambda x: x[0] != '#', body.split()))
        post.save()
        return post


class UserForm(forms.ModelForm):
    web_site = forms.CharField(required=False)

    class Meta:
        model = User
        fields = [
            'full_name', 'username', 'web_site',
            'biography', 'email', 'phone'
        ]


class UserNotificationForm(forms.ModelForm):
    like_notification = forms.ChoiceField(
        choices=LIKE, widget=forms.RadioSelect())
    comment_notification = forms.ChoiceField(
        choices=COMMENT, widget=forms.RadioSelect())
    comment_like_notification = forms.ChoiceField(
        choices=COMMENT_LIKE, widget=forms.RadioSelect())
    follow_request_notification = forms.ChoiceField(
        choices=FOLLOW_REQUEST, widget=forms.RadioSelect())

    class Meta:
        model = User
        fields = [
            'like_notification', 'comment_notification', 'comment_like_notification',
            'follow_request_notification'
        ]


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['image',]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(StoryForm, self).__init__(*args, **kwargs)
  
    def save(self, commit=True):
        story = super(StoryForm, self).save(commit=False)
        story.user = self.request.user
        story.save()
        return story
