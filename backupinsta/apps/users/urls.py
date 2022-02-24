from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    # custom admin pages
    path('admin/user_detail/<int:user_id>/pdf/', views.admin_user_pdf, name='admin_user_pdf'),
    path('admin/user_detail/<int:user_id>/', views.admin_user_detail, name='admin_user_detail'),

    # user auth 
    path('signin/', views.UserSignInView.as_view(), name='sign-in'),
    path('signup/', views.UserRegisterView.as_view(), name='sign-up'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('password-reset/', views.password_reset, name='password-reset'),
    path('password-set/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),

    # user page
    path('<username>/', views.profile, name='profile'),

]
