from django.urls import include, path

from . import views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('accounts/password_change/', views.change_password,
         name='my_password_change'),
    path('accounts/', include('django.contrib.auth.urls')),
]
