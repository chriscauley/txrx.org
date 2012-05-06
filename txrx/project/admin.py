from django.contrib import admin
from lablackey.article.admin import ArticleAdmin
from models import Project, NewsItem

class NewsItemAdmin(ArticleAdmin):
    pass

class ProjectAdmin(ArticleAdmin):
    pass

admin.site.register(NewsItem,ArticleAdmin)
admin.site.register(Project,ProjectAdmin)
