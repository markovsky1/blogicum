from django.shortcuts import render, get_object_or_404

from .models import Post, Category
from .constants import POSTS_ON_HOME_PAGE


def index(request):

    post_list = Post.objects.published()[:POSTS_ON_HOME_PAGE]

    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.published(),
        id=post_id
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    desired_category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    post_list = desired_category.posts.published()
    return render(
        request,
        'blog/category.html',
        {'category': desired_category, 'post_list': post_list}
    )
