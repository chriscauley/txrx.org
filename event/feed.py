from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from .models EventOccurrence

class LatestEntriesFeed(Feed):
  title = "Chicagocrime.org site news"
  link = "/sitenews/"
  description = "Updates on changes and additions to chicagocrime.org."

  def items(self):
    return NewsItem.objects.order_by('-pub_date')[:5]

  def item_title(self, item):
    return item.title

  def item_description(self, item):
    return item.description

  # item_link is only needed if NewsItem has no get_absolute_url method.
  def item_link(self, item):
    return reverse('news-item', args=[item.pk])
