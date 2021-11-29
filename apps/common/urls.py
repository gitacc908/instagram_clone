from django.urls import path
from . import views



urlpatterns = [
 
    path('', views.main, name='index'),
    path('post_detail', views.post_detail, name='post_detail'),
    path('edit_profile', views.edit_profile, name='edit_profile'),


    # ajax requests
    path('post/', views.PostView.as_view(), name='post'),

    path('like/', views.LikeView.as_view(), name='like'),
    path('save/', views.SaveView.as_view(), name='save'),
    path('comment/', views.CommentView.as_view(), name='comment'),
    path('follow/', views.FollowView.as_view(), name='follow'),

]
    