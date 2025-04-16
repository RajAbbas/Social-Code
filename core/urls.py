from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name="post-list"),
    path('register/',views.register,name="register"),
    path('login/',views.login_page,name='login'),
    path('post-form/',views.post_form,name="post-form"),
    path('logout/',views.logout_user,name="logout"),
    path('post-detail/<int:pk>/',views.post_detail,name='post-detail'),
    path('post-detail/<int:pk>/like/',views.like_dislike_post,{'vote_type' : 'like'},name='like-post'),
    path('post-detail/<int:pk>/dislike/',views.like_dislike_post,{'vote_type' : 'dislike'},name='dislike-post'),
    path('save-post/<int:post_id>/' ,views.save_post, name="save-post"),
    path('saved-posts-list/' ,views.saved_posts_list, name="saved-posts-list"),
]
    