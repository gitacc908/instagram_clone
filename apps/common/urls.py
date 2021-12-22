from django.urls import path
from . import views



urlpatterns = [
 
    path('', views.main, name='index'),
    path('post_detail/<int:pk>/', views.post_detail, name='post_detail'),
    path('edit_profile', views.edit_profile, name='edit_profile'),


    # ajax requests
    path('post/', views.PostView.as_view(), name='post'),

    path('like/', views.LikePostView.as_view(), name='like'),
    path('like_comment/', views.LikeCommentView.as_view(), name='like_comment'),
    path('save/', views.SaveView.as_view(), name='save'),
    path('comment/', views.CommentView.as_view(), name='comment'),
    path('reply/', views.CommentReplyView.as_view(), name='reply'),
    path('follow/', views.FollowView.as_view(), name='follow'),
    path('avatar/', views.UpdateAvatarView.as_view(), name='avatar'),

]
    