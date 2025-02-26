from django.urls import path, include

from blog import views

app_name = 'blog'


"""
Я поменял <int:pk> на <int:post_id>, но меня не пустили тесты 😢😢😢
"""
post_endpoints = [
    path('create/', views.PostCreateView.as_view(), name='create_post'),
    path(
        '<int:pk>/',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        '<int:pk>/edit/',
        views.PostUpdateView.as_view(),
        name='edit_post'
    ),
    path(
        '<int:pk>/delete/',
        views.PostDeleteView.as_view(),
        name='delete_post'
    ),
    path(
        '<int:pk>/comment/',
        views.CommentCreateView.as_view(),
        name='add_comment'
    ),
    path(
        '<int:pk>/edit_comment/<int:comment_id>',
        views.CommentUpdateView.as_view(),
        name='edit_comment'
    ),
    path(
        '<int:pk>/delete_comment/<int:comment_id>',
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
