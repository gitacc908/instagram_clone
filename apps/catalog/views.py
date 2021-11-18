from django.shortcuts import render
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from apps.users.models import User
from apps.catalog.models import Post, Image
from django.views import View
from apps.catalog.forms import PostForm


class PostView(View):
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        print(form, request.POST.get('images'))
        if form.is_valid():
            post = form
            form.author = request.user
            form.save()
        Image.objects.bulk_create([
            Image(post=post, image=image) for image in request.POST.get('image') 
        ])

        return JsonResponse({'status': 'shared'})
        # return JsonResponse({'status': 'error'}, status=404)