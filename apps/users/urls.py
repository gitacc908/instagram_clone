from django.urls import path
from . import views


urlpatterns = [
 
    path('', views.main, name='index'),
   
    # user auth 
    path('signin/', views.UserSignInView.as_view(), name='sign-in'),
    path('signup/', views.UserRegisterView.as_view(), name='sign-up'),
    # path('')
]
