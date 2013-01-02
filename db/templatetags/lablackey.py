from django import template
from django.conf import settings
from sorl.thumbnail import get_thumbnail

register = template.Library()

@register.simple_tag
def list_model(model_name,args):
    values = load_defaults(dict(query="all()",limit=":",select_related=False))
    model = __import__(model)
    qs = getattr(model.objects,values['query'])[values['limit']]
    if values['select_related']:
        qs = qs.select_related()
    return qs

def load_defaults(values,args):
    """
    Loads a string of "k1=v1,k2=v2..." into a dictionary of default values.
    Basically just compensates for simple_tags lack of *args and **kwargs.
    Probably not the best way to handle this.
    Holds the world record for most inappropriately long doc-string,
    if only by one line.
    """
    if args:
        values.update(dict([a.split("=") for a in args.split(",")]))
    return values
