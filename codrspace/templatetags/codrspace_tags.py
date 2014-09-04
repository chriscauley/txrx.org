#! This entire file can be depracated 9/2014
from django.template import Library, TemplateSyntaxError, Variable, Node
from django.template.defaulttags import token_kwargs
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.conf import settings
from codrspace.utils import localize_date
from codrspace.models import Setting

register = Library()

@register.filter(name='localize')
def localize(dt, user):
    if not dt:
        return None
    from_tz = settings.TIME_ZONE
    to_tz = "US/Central"

    # get the users timezone
    if not user.is_anonymous():
        user_settings = Setting.objects.get(user=user)
        to_tz = user_settings.timezone

    return localize_date(dt, from_tz=from_tz, to_tz=to_tz)

class RandomBlogNode(Node):
    def render(self, context):
        random_user = User.objects.order_by('?')[0]
        return reverse('post_list', args=[random_user.username])

@register.tag
def random_blog(parser, token):
    """
    Get a random bloggers post list page
    {% random_blog %}
    """
    return RandomBlogNode()

@register.inclusion_tag("lastest_posts.html", takes_context=True)
def latest_posts(context, amount):
    posts = Post.objects.filter(status="published").order_by('-publish_dt')
    if posts:
        posts = posts[:int(amount)]
    context.update({
        'posts': posts
    })
    return context
