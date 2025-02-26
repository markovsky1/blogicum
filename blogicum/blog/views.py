from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse

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
    queryset = Post.objects.published().comment_count().order_by('-pub_date')
    template_name = 'blog/index.html'
    paginate_by = POSTS_ON_HOME_PAGE


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'pk'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.author == self.request.user:
            return obj
        return super().get_object(Post.objects.published())

    def get_context_data(self, **kwargs):
        return dict(
            **super().get_context_data(**kwargs),
            form=CommentForm(),
            comments=self.object.comments.select_related('author'),
        )


class CategoryDetailView(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = POSTS_ON_CATEGORY_PAGE
    _category = None

    def get_category(self):
        if self._category is None:
            self._category = get_object_or_404(
                Category,
                slug=self.kwargs['category_slug'],
                is_published=True
            )
        return self._category

    def get_queryset(self):
        return self.get_category().posts.published()

    def get_context_data(self, **kwargs):
        return dict(
            super().get_context_data(**kwargs),
            category=self.get_category(),
        )


class ProfileDetailView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = POSTS_ON_PROFILE_PAGE
    _profile = None

    def get_profile(self):
        if self._profile is None:
            self._profile = get_object_or_404(
                User,
                username=self.kwargs['username']
            )
        return self._profile

    def get_queryset(self):
        user_posts = self.get_profile().posts
        queryset = user_posts.published()
        if self.request.user == self.get_profile():
            queryset = user_posts
        return queryset.comment_count().order_by('-pub_date')

    def get_context_data(self, **kwargs):
        return dict(
            super().get_context_data(**kwargs),
            profile=self.get_profile()
        )


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'username', 'email']
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse(
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
        return reverse(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class PostUpdateView(OnlyAuthorMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'pk'

    def handle_no_permission(self):
        return redirect('blog:post_detail', pk=self.get_object().pk)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(OnlyAuthorMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')
    template_name = 'blog/create.html'

    def get_object(self, queryset=None):
        """Получение поста по `pk`, а не `pk`."""
        return get_object_or_404(Post, id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = PostForm(instance=self.get_object())  # Создаем форму с объектом
        context['form'] = form  # Передаем форму в контекст
        return context


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
        return reverse(
            'blog:post_detail', kwargs={'pk': self.kwargs['pk']}
        )


class CommentUpdateView(OnlyAuthorMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def get_object(self, queryset=None):
        """Получение комментария по `comment_id`, а не `pk`."""
        return get_object_or_404(Comment, id=self.kwargs['comment_id'])

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'pk': self.object.post.pk}
        )


class CommentDeleteView(OnlyAuthorMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'

    def get_object(self, queryset=None):
        """Получение комментария по `comment_id`, а не `pk`."""
        return get_object_or_404(Comment, id=self.kwargs['comment_id'])

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'pk': self.object.post.pk}
        )
