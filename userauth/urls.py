from django.contrib import admin
from django.urls import path
from socialmedia import settings
from userauth import views
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home),
    path('login/',views.login),
    path('signup/',views.signup),
    path('logout/',views.logout_view),
    path('upload',views.upload),
    path('like-post/<str:id>', views.likes, name='like-post'),
    path('post/<str:id>', views.home_post, name='post-detail'),
    path('explore',views.explore),
    path('profile/<str:id_user>', views.profile),
    path('delete/<str:id>', views.delete),
    path('search-results/', views.search_results, name='search_results'),
    path('follow', views.follow, name='follow'),
    path('comment/add/<uuid:post_id>/', views.add_comment, name='add_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]
