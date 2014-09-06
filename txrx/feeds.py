from django.conf import settings
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse

from blog.models import Post
from course.models import Session
from event.models import EventOccurrence

import datetime

class AllFeed(Feed):
  title = settings.SITE_NAME
  link = "/rss/"
  description = "New classes, blogs and events for %s"%title

  def items(self):
    kwargs = {'publish_dt__lte': datetime.datetime.now()}
    sessions = list(Session.objects.filter(**kwargs)[:5])
    posts = list(Post.objects.filter(**kwargs)[:5])
    events = list(EventOccurrence.objects.filter(**kwargs)[:5])
    return sorted(sessions+posts+events,key=lambda i: i.publish_dt,reverse=True)

  def item_title(self, item):
    if isinstance(item,Post):
      before = "Blog Post: "
    if isinstance(item,Session):
      before = "New Class: "
    if isinstance(item,EventOccurrence):
      before = "Upcoming Event: "
    return before + str(item)

  def item_description(self, item):
    return item.description
