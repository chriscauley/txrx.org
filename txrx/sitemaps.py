from django.contrib.sitemaps import Sitemap
from blog.models import Post
from course.models import Course

import datetime

class BlogSitemap(Sitemap):
  changefreq = "never"
  priority = 0.5

  def items(self):
    return Post.objects.filter(status="published",publish_dt__lte=datetime.datetime.now())

  def lastmod(self, obj):
    return obj.publish_dt

class CourseSitemap(Sitemap):
  changefreq = "never"
  priority = 0.5

  def items(self):
    return Course.objects.all()

  def lastmod(self, obj):
    return datetime.datetime.now()

sitemaps = {
  'blog': BlogSitemap,
  #'classes': CourseSitemap,
}
