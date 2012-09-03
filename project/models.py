from django.db import models
from lablackey.profile.models import UserModel
from articles.models import Article, ArticleManager
#from tool.models import Tool
#from course.models import Course

class Project(Article):
    _feed_label = "Project Spotlight"
    objects = ArticleManager()

class NewsItem(Article):
    _feed_label = "News"
    objects = ArticleManager()
