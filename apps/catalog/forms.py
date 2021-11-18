from django import forms
from apps.catalog.models import Post, Image


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body', 'comments_on')
