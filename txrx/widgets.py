from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.contrib.admin.widgets import AdminFileWidget

import urllib

class CKEditor (forms.Textarea):
    class Media:
        js = (
            '/static/js/jquery-1.6.2.min.js',
            '/static/js/ckeditor/ckeditor_basic.js',
        )
        
    def render(self, name, value, attrs=None):
        rendered = super(CKEditor, self).render(name, value, attrs)
        return mark_safe('<div style="clear: both; margin-bottom: 2px;"/></div>') + rendered + mark_safe('<script type="text/javascript">jQuery(document).ready(function () { CKEDITOR.replace( \'id_' + name + '\', {skin : \'office2003\', customConfig : \'/site_media/javascript/ckeditor_config1.js\'} ); })</script>')
