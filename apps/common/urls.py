from django.urls import path
from . import views



urlpatterns = [
 
    path('', views.main, name='index'),

    # ajax requests
    path('like/', views.LikeView.as_view(), name='like'),
    path('save/', views.SaveView.as_view(), name='save'),
    path('comment/', views.CommentView.as_view(), name='comment'),
]
    