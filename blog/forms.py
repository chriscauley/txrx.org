from django.conf import settings
from django.contrib import admin
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.core.exceptions import ObjectDoesNotExist
from django import forms

from .models import Post
from .utils import localize_date
from media.models import Photo

import datetime

from tagging.forms import TagField
from tagging.models import Tag

from wmd.widgets import MarkDownInput

class TaggedModelForm(forms.ModelForm):
  """Provides an easy mixin for adding tags using django-tagging"""
  tags = TagField(help_text="Separate tags with commas. Input will be lowercased")
  def __init__(self,*args,**kwargs):
    super(TaggedModelForm,self).__init__(*args,**kwargs)
    instance = kwargs.get('instance',None)
    initial = kwargs.get('initial',{})
    if instance and not initial.get('tags',None):
      self.fields['tags'].initial = ','.join([t.name for t in Tag.objects.get_for_object(instance)])
  def save(self,*args,**kwargs):
    instance = super(TaggedModelForm,self).save(*args,**kwargs)
    if not kwargs.get('commit',True):
      return instance
    Tag.objects.update_tags(instance,self.cleaned_data['tags'])
    return instance
  class Meta:
    abstract = True

class PostForm(TaggedModelForm):
  content = forms.CharField(widget=MarkDownInput(),required=False)
  photo = forms.ModelChoiceField(Photo.objects.all(),required=False)
  class Meta:
    model = Post
    fields = ('title','slug','content','short_content','publish_dt','tags','status','photo')

  def clean_slug(self):
    slug = self.cleaned_data['slug']
    if self.instance:
      if Post.objects.filter(slug=slug, user=self.user).exclude(pk=self.instance.pk).count():
        raise forms.ValidationError('You already have a post with this slug')
    return slug

  def clean_tags(self):
    tags = self.cleaned_data['tags']
    if not ',' in tags:
      tags = tags + ','
    return tags

  def save(self,*args,**kwargs):
    try:
      self.instance.user
    except ObjectDoesNotExist:
      self.instance.user = self.user
    return super(PostForm,self).save(*args,**kwargs)

  def __init__(self, *args, **kwargs):
    # checking for user argument here for a more
    # localized form
    self.user = None
    self.timezone = None
    if kwargs.get('instance',None):
      kwargs['initial'] = kwargs.pop('initial',{})
      kwargs['initial']['publish_dt'] = kwargs['instance'].publish_dt

    if 'user' in kwargs:
      self.user = kwargs.pop('user', None)
    super(PostForm, self).__init__(*args, **kwargs)
    self.fields['slug'].help_text = "URL will be /blog/your-name/<b>slug-goes-here</b>/"
    self.fields['tags'].help_text = "Separate tags with commas. Input will be lowercased."
    self.fields['publish_dt'].help_text = "<i>YYYY-MM-DD HH:MM</i> (24-hour time)"
    self.fields['photo'].widget=ForeignKeyRawIdWidget(Post._meta.get_field("photo").rel,admin.site)
    # add span class to charfields
    for field in self.fields.values():
      if isinstance(field, forms.fields.CharField):
        if 'class' in field.widget.attrs:
          field.widget.attrs['class'] = "%s %s" % (
            field.widget.attrs['class'],
            'span8',
          )
        else:
          field.widget.attrs['class'] = 'span8'
