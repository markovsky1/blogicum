from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView, DetailView
)

from .models import Post, Category
from .constants import POSTS_ON_HOME_PAGE, POSTS_ON_CATEGORY_PAGE


class HomePage(ListView):
    model = Post
    queryset = Post.objects.published()
    template_name = 'blog/index.html'
    paginate_by = POSTS_ON_HOME_PAGE


class PostDetailView(DetailView):
    model = Post
    queryset = Post.objects.published()
    template_name = 'blog/detail.html'


class CategoryDetailView(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = POSTS_ON_CATEGORY_PAGE

    def get_queryset(self):
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return self.category.posts.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
