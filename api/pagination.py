from rest_framework import pagination
from rest_framework.response import Response

class LinkHeaderPagination(pagination.PageNumberPagination):
  def get_paginated_response(self, data, **kwargs):
    next_url = self.get_next_link()
    previous_url = self.get_previous_link()

    if next_url is not None and previous_url is not None:
      link = '<{next_url}>; rel="next", <{previous_url}>; rel="prev"'
    elif next_url is not None:
      link = '<{next_url}>; rel="next"'
    elif previous_url is not None:
      link = '<{previous_url}>; rel="prev"'
    else:
      link = ''

    link = link.format(next_url=next_url, previous_url=previous_url)
    kwargs['headers'] = kwargs.get('headers',{})
    if link:
      kwargs['link'] = link

    return Response(data, **kwargs)

def paginate_response(queryset,request,**kwargs):
  p = LinkHeaderPagination()
  data = p.paginate_queryset(queryset,request)
  return p.get_paginated_response(data,**kwargs)
