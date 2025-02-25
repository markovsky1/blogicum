from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.db.models import Count

from .forms import PostForm, CommentForm
from .models import Post, Category, Comment
from .constants import (
    POSTS_ON_HOME_PAGE, POSTS_ON_CATEGORY_PAGE, POSTS_ON_PROFILE_PAGE
)


User = get_user_model()


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class HomePage(ListView):
    model = Post
    queryset = Post.objects.published().annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')
    template_name = 'blog/index.html'
    paginate_by = POSTS_ON_HOME_PAGE


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Post.objects.published()
        return Post.objects.published() | Post.objects.filter(author=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context


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


class ProfileDetailView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = POSTS_ON_PROFILE_PAGE


    def get_queryset(self):
        self.profile = get_object_or_404(
            User,
            username = self.kwargs['username']
        )
        user = self.request.user
        if user == self.profile:
            return self.profile.posts.all().annotate(
                comment_count=Count('comments')
            ).order_by('-pub_date')
        return self.profile.posts.published().annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'username', 'email']
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})


class PostUpdateView(OnlyAuthorMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def handle_no_permission(self):
        return redirect('blog:post_detail', pk=self.get_object().pk)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(OnlyAuthorMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')


class CommentCreateView(LoginRequiredMixin, CreateView):
    commenting_post = None
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        self.commenting_post = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.commenting_post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.kwargs['pk']})


class CommentUpdateView(OnlyAuthorMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def get_object(self, queryset=None):
        """Получение комментария по `comment_id`, а не `pk`."""
        return get_object_or_404(Comment, id=self.kwargs['comment_id'])

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.post.pk})


class CommentDeleteView(OnlyAuthorMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'

    def get_object(self, queryset=None):
        """Получение комментария по `comment_id`, а не `pk`."""
        return get_object_or_404(Comment, id=self.kwargs['comment_id'])

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.post.pk})
