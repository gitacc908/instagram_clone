from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
 
#    path('users/<username>/', views.user_detail, name='user_detail'),

    path('profile/', views.profile, name='profile'),

    # user auth 
    path('signin/', views.UserSignInView.as_view(), name='sign-in'),
    path('signup/', views.UserRegisterView.as_view(), name='sign-up'),
    
    path('password-reset/', views.password_reset, name='password-reset'),
    path('password-set/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    # path('password-reset/', views.ResetPasswordView.as_view(), name='password_reset'),
    # path('password-reset-confirm/<uidb64>/<token>/',
    #     auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
    #     name='password_reset_confirm'),

]
    