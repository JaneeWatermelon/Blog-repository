from django.contrib import admin

from news.models import Category, Comment, News


class CommentAdmin(admin.TabularInline):
    model = Comment
    fields = (('user', 'time'), ('likes', 'dislikes'), 'text')
    readonly_fields = ('time',)
    extra = 0
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'likes', 'views', 'time', 'category')
    readonly_fields = ('time',)
    search_fields = ('time',)
    inlines = (CommentAdmin,)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

