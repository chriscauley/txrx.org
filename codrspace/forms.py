from django.conf import settings
from django.contrib.admin import widgets
from django import forms

from codrspace.models import Post, Media, Setting
from codrspace.utils import localize_date

from datetime import datetime

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'wmd-input'}),required=False)

    class Meta:
        model = Post
        exclude = ('author',)

    class Media:
        js = ('grappelli/js/grappelli.min.js',)

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        count = Post.objects.filter(slug=slug, author=self.user).count()

        if count > 0:
            if self.instance:
                posts = Post.objects.filter(slug=slug, author=self.user)
                for post in posts:
                    if post.pk == self.instance.pk:
                        return slug

            msg = 'You already have a post with this slug'
            raise forms.ValidationError(msg)

        return slug

    def __init__(self, *args, **kwargs):
        # checking for user argument here for a more
        # localized form
        self.user = None
        self.timezone = None

        if 'user' in kwargs:
            self.user = kwargs.pop('user', None)

        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['publish_dt'].widget = widgets.AdminSplitDateTime()

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

class MediaForm(forms.ModelForm):

    class  Meta:
        model = Media


class SettingForm(forms.ModelForm):

    class  Meta:
        model = Setting

    def __init__(self, *args, **kwargs):
        super(SettingForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            if isinstance(field, forms.fields.CharField):
                field.widget.attrs.update({'class': 'span10'})


class FeedBackForm(forms.Form):
    email = forms.EmailField(required=True)
    comments = forms.CharField(widget=forms.Textarea(), required=True)

    def __init__(self, *args, **kwargs):
        super(FeedBackForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            if isinstance(field, forms.fields.CharField):
                field.widget.attrs.update({'class': 'span10'})
