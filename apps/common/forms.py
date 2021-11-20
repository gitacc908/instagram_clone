from django import forms
from apps.catalog.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body', 'comments_off')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PostForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        post = super(PostForm, self).save(commit=False)
        post.author = self.request.user
        post.comments_off = True if self.cleaned_data.get('comments_off') == 'true' else False
        post.save()
        return post
