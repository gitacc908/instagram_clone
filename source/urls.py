from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns


urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path('account/', include('apps.users.urls')),
    path('catalog/', include('apps.catalog.urls')),
    path('chat/', include('apps.chat.urls')),
    path('emoji/', include('emoji.urls')),

    path('', include('apps.common.urls')),

)
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

# if settings.DEBUG:
#     urlpatterns += static(
#         settings.STATIC_URL, document_root=settings.STATIC_ROOT
#     )
#     urlpatterns += static(
#         settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
#     )
