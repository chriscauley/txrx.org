from django import forms
from django.db import models
from django.conf import settings

class LocationPickerWidget(forms.TextInput):
    class Media:
        css = {
            'all': (
                settings.STATIC_URL + 'location/location_picker.css',
            )
        }
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js',
            '//www.google.com/jsapi?key=' + settings.MAPS_API_KEY,
            settings.STATIC_URL + 'location/jquery.location_picker.js',
        )

    def __init__(self, language=None, attrs=None):
        self.language = language or settings.LANGUAGE_CODE[:2]
        super(LocationPickerWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        if None == attrs:
            attrs = {}
        attrs['class'] = 'location_picker'
        return super(LocationPickerWidget, self).render(name, value, attrs)

class LocationField(models.CharField):

    def formfield(self, **kwargs):
        kwargs['widget'] = LocationPickerWidget
        return super(LocationField, self).formfield(**kwargs)
