from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path


app_name = 'recipe_community'

urlpatterns = [
    path('', include('recipes.urls')),
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
]

urlpatterns += [
    path('about/', views.flatpage, {'url': '/about/'}, name='about'),
    path('tech/', views.flatpage, {'url': '/tech/'}, name='tech'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

handler404 = "recipe_community.views.page_not_found"  # noqa
handler500 = "recipe_community.views.server_error"  # noqa
