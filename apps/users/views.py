from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import RegisterForm

def main(request):
    # return render(request, 'main/index.html')
    form = RegisterForm()
    return render(request, 'users/register.html',{'form':form})
