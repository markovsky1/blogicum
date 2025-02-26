from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.html import format_html

from .models import Post, Category, Location, Comment

admin.site.empty_value_display = 'Не задано'
admin.site.unregister(Group)


class PostInline(admin.StackedInline):
    model = Post
    extra = 1


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'post_image',
        'author',
        'category',
        'location',
        'comment_count',
        'is_published',
        'pub_date',
        'created_at',
    )
    list_editable = ('is_published',)
    search_fields = ('title', 'text')
    list_filter = (
        'is_published',
        'category',
        'location',
        'pub_date',
        'created_at'
    )
    date_hierarchy = 'pub_date'

    @admin.display(description='Количество комментариев')
    def comment_count(self, obj):
        return Comment.objects.filter(post=obj).count()

    @admin.display(description='Изображение')
    def post_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" " />', obj.image.url
            )
        return 'Нет изображения'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    list_display = ('title', 'is_published', 'created_at')
    list_editable = ('is_published',)
    search_fields = ('title',)
    list_filter = ('is_published', 'created_at')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    list_display = ('name', 'is_published', 'created_at')
    list_editable = ('is_published',)
    search_fields = ('name',)
    list_filter = ('is_published', 'created_at')
