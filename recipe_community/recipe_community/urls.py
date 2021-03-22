"""recipe_community URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
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
