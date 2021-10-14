from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
# from django.views.generic import TemplateView
# from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, DeleteView, UpdateView, CreateView
# from django.views.generic.list import ListView
# from django.urls import reverse

from apps.users.models import User
from .forms import RegisterForm, LoginForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login


def main(request):
    return render(request, 'main/index.html')


class UserSignInView(View):
    form_class = LoginForm
    template_name = 'users/registration/login.html'
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username_email_phone')
            password = form.cleaned_data.get('password')
            user = authenticate(
                self.request, username=username, 
                password=password
            )
            if user:
                login(self.request, user)
                return redirect(self.success_url)
        return render(request, self.template_name)


class UserRegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users/registration/register.html'
    success_url = '/'
