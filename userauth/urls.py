from django.contrib import admin
from django.urls import path
from socialmedia import settings
from userauth import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('upload', views.UploadPostView.as_view(), name='upload'),
    path('like-post/<str:id>', views.LikePostView.as_view(), name='like-post'),
    path('post/<str:id>', views.SinglePostView.as_view(), name='post-detail'),
    path('explore', views.ExploreView.as_view(), name='explore'),
    path('profile/<str:id_user>', views.ProfileView.as_view(), name='profile'),
    path('delete/<str:id>', views.DeletePostView.as_view(), name='delete'),
    path('search-results/', views.SearchResultsView.as_view(), name='search_results'),
    path('follow', views.FollowView.as_view(), name='follow'),
    path('comment/add/<uuid:post_id>/', views.AddCommentView.as_view(), name='add_comment'),
    path('comment/delete/<int:comment_id>/', views.DeleteCommentView.as_view(), name='delete_comment'),
    path('tags/', views.ManageTagsView.as_view(), name='manage_tags'),
    path('tag/<str:tag_name>/', views.TagPostsView.as_view(), name='tag_posts'),
    path('tag/delete/<int:tag_id>/', views.DeleteTagView.as_view(), name='delete_tag'),
    path('bookmark-post/<str:id>', views.BookmarkView.as_view(), name='bookmark-post'),
    path('bookmarks/', views.BookmarksView.as_view(), name='bookmarks'),
]
