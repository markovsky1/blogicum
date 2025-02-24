from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.HomePage.as_view(), name='index'),
    path(
        'posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'
    ),
    path(
        'category/<slug:category_slug>/',
        views.CategoryDetailView.as_view(),
        name='category_posts'),
]
