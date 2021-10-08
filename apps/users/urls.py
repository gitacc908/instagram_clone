from django.urls import path
from . import views


urlpatterns = [
    # admin pages
    path('', views.main, name='index'),
]
