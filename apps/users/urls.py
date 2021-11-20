from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
 
    path('<username>/', views.profile, name='profile'),

    # user auth 
    path('signin/', views.UserSignInView.as_view(), name='sign-in'),
    path('signup/', views.UserRegisterView.as_view(), name='sign-up'),
    
    path('password-reset/', views.password_reset, name='password-reset'),
    path('password-set/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
    