from django.db import models
from django.contrib.auth import get_user_model

from core.models import CreatedPublishedModel
from .querysets import PostQuerySet
from .constants import MAX_LENGTH_TITLE, MAX_LENGTH_NAME, CATEGORY_TITLE_SLICE


User = get_user_model()


class Category(CreatedPublishedModel):
    title = models.CharField(
        max_length=MAX_LENGTH_TITLE,
        null=False,
        verbose_name='Заголовок'
    )
    description = models.TextField(
        null=False,
        verbose_name='Описание'
    )
    slug = models.SlugField(
        unique=True,
        null=False,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; разрешены символы латиницы, '
            'цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        default_related_name = 'categories'

    def __str__(self):
        return self.title[:CATEGORY_TITLE_SLICE]


class Location(CreatedPublishedModel):
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        null=False,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'
        default_related_name = 'locations'

    def __str__(self):
        return self.name


class Post(CreatedPublishedModel):
    title = models.CharField(
        max_length=MAX_LENGTH_TITLE,
        verbose_name='Заголовок',
        null=False
    )
    text = models.TextField(
        null=False,
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        null=False,
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    image = models.ImageField('Фото', blank=True)

    objects = PostQuerySet.as_manager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']
        default_related_name = 'posts'

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField('Комментарий')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)
