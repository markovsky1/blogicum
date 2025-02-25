from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Post, Category, Location

admin.site.empty_value_display = 'Не задано'
# User = get_user_model()
admin.site.unregister(Group)
# admin.site.unregister(User)


# @admin.register(User)
# class CustomAdmin(UserAdmin):
#     list_display = UserAdmin.list_display + ('post_count',)

#     @admin.display(description='Количество постов')
#     def post_count(self, obj):
#         return obj.posts.count()


class PostInline(admin.StackedInline):
    model = Post
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'category',
        'location',
        'is_published',
        'pub_date',
        'created_at'
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
