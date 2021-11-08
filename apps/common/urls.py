from django.urls import path
from . import views



urlpatterns = [
 
    # path('', views.main, name='ndex'),
   
    path('', views.main, name='index'),
    path('like/', views.LikeView.as_view(), name='like'),


]
    