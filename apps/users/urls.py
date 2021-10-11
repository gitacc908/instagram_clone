from django.urls import path
from . import views


urlpatterns = [
    # admin pages
    path('', views.main, name='index'),

    # user auth 
    path('signup/', views.UserRegisterView.as_view(), name='sign-up'),
    # path('')
]
