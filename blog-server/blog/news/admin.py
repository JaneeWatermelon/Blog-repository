from django.contrib import admin

from news.models import Category, Comment, News


class CommentAdmin(admin.TabularInline):
    model = Comment
    fields = (('user', 'time'), ('likes', 'dislikes'), 'text')
    readonly_fields = ('time',)
    extra = 0
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'likes', 'views', 'name', 'time', 'category')
    readonly_fields = ('time',)
    search_fields = ('time',)
    ordering = ('name',)
    inlines = (CommentAdmin,)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

