from django.urls import path, include

from blog import views

app_name = 'blog'


post_endpoints = [
    path('create/', views.PostCreateView.as_view(), name='create_post'),
    path(
        '<int:post_id>/',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        '<int:post_id>/edit/',
        views.PostUpdateView.as_view(),
        name='edit_post'
    ),
    path(
        '<int:post_id>/delete/',
        views.PostDeleteView.as_view(),
        name='delete_post'
    ),
    path(
        '<int:post_id>/comment/',
        views.CommentCreateView.as_view(),
        name='add_comment'
    ),
    path(
        '<int:post_id>/edit_comment/<int:comment_id>',
        views.CommentUpdateView.as_view(),
        name='edit_comment'
    ),
    path(
        '<int:post_id>/delete_comment/<int:comment_id>',
        views.CommentDeleteView.as_view(),
        name='delete_comment'
    ),
]

category_endpoints = [
    path(
        '<slug:category_slug>/',
        views.CategoryDetailView.as_view(),
        name='category_posts'),
]

profile_endpoints = [
    path(
        '<slug:username>/',
        views.ProfileDetailView.as_view(),
        name='profile'
    ),
]
urlpatterns = [
    path('', views.HomePage.as_view(), name='index'),
    path('posts/', include(post_endpoints)),
    path('category/', include(category_endpoints)),
    path('profile/', include(profile_endpoints)),
    path(
        'edit_profile/',
        views.ProfileUpdateView.as_view(),
        name='edit_profile'
    ),
]
