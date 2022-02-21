from django.urls import path
from . import views


urlpatterns = [
    # path('room/<int:user_id>/', views.course_chat_room,
    # name='course_chat_room'),
    path('direct/<user>/', views.direct, name='dm_user'),
    path('direct/', views.direct, name='direct'),
]
