from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeAllView.as_view(), name='index'),
    path('recipe/<int:pk>/', views.RecipeDetailView.as_view(),
         name='recipe_detail'),
    path('recipe/create/', views.RecipeCreateView.as_view(),
         name='recipe_create'),
    path('recipe/<int:pk>/update/', views.RecipeUpdateView.as_view(),
         name='recipe_update'),
    path('recipe/<int:pk>/delete/', views.RecipeDeleteView.as_view(),
         name='recipe_delete'),
    path('profile/<int:pk>/', views.ProfileView.as_view(),
         name='profile'),
    path('<str:username>/follow/', views.FollowChangeView.as_view(),
         name='profile_follow'),
    path('subcriptions/', views.SubscriptionListView.as_view(),
         name='subcriptions'),
    path('bookmarks/', views.BookmarksListView.as_view(),
         name='bookmarks'),
    path('<int:pk>/favorites/', views.BookmarkChangeView.as_view(),
         name='recipe_bookmark'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('<int:pk>/order/', views.OrderChangeView.as_view(),
         name='recipe_order'),
    path('download/', views.orders_view, name='orderlist')
]
