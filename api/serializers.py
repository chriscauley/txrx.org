from django.core.paginator import Paginator, InvalidPage
from django.db.models import QuerySet

from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param

import six, copy

class PaginatedListSerializer(serializers.ListSerializer):
  def __init__(self,request,*args,**kwargs):
    self.request = request
    child = kwargs.get('child', copy.deepcopy(self.child))
    queryset = child.get_queryset(request)
    paginator = Paginator(queryset, child.page_size)
    self.page_query_param = child.page_query_param
    page_number = request.query_params.get(self.page_query_param, 1)

    try:
      self.page = paginator.page(page_number)
    except InvalidPage as exc:
      msg = class_.invalid_page_message.format(
        page_number=page_number, message=six.text_type(exc)
      )
      raise NotFound(msg)
    super(PaginatedListSerializer,self).__init__(list(self.page),*args,**kwargs)

  def get_next_link(self):
    if not self.page.has_next():
      return None
    url = self.request.build_absolute_uri()
    page_number = self.page.next_page_number()
    return replace_query_param(url, self.page_query_param, page_number)

  def get_previous_link(self):
    if not self.page.has_previous():
      return None
    url = self.request.build_absolute_uri()
    page_number = self.page.previous_page_number()
    if page_number == 1:
      return remove_query_param(url, self.page_query_param)
    return replace_query_param(url, self.page_query_param, page_number)

  def get_paginated_response(self):
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
    headers = {'Link': link} if link else {}

    return Response(self.data, headers=headers)

class BaseSizzler(serializers.ModelSerializer):
  permissions = classmethod(lambda class_,request: request.user.is_staff)
  get_queryset = classmethod(lambda class_,request=None: class_.Meta.model.objects.all())
  many = False
  page_size = 50
  page_query_param = 'page'
  @classmethod
  def many_init(cls, *args, **kwargs):
    kwargs['child'] = cls()
    kwargs['child'].many = True
    return PaginatedListSerializer(*args, **kwargs)

  def get_field_names(self,*args,**kwargs):
    #if getattr(self,'_many'):
    #  return ['__unicode__',self.Meta.model._meta.pk.name]
    pk_name = self.Meta.model._meta.pk.name
    fields = list(super(BaseSizzler,self).get_field_names(*args,**kwargs))

    #! TODO This should maybe use pk_name once schema is in use?
    if not "pk" in fields:
      fields.append("pk")
    if not "__unicode__" in fields:
      fields.append("__unicode__")
    return fields

  def get_fields(self,*args,**kwargs):
    fields = super(BaseSizzler,self).get_fields(*args,**kwargs)
    return fields
