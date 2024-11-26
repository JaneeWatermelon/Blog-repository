from django.contrib import admin

from news.models import Category, Comment, News, AllNewsURLs


@admin.action(description="Добавить url выбранных новостей в модель всех url")
def add_news_urls(modeladmin, request, queryset):
    all_news_urls = AllNewsURLs.objects.first()
    for news in queryset:
        if news.url not in all_news_urls.urls:
            all_news_urls.urls += [news.url]
            all_news_urls.save()

@admin.register(AllNewsURLs)
class AllNewsURLsAdmin(admin.ModelAdmin):
    list_display = ('id', 'urls')

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
    inlines = (CommentAdmin,)
    actions = (add_news_urls,)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

