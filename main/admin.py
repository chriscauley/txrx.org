from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin

admin.site.unregister(FlatPage)

class FlatPageAdmin(FlatPageAdmin):
  class Media:
    js = ['/static/admin/js/core.js', '/static/admin/js/admin/RelatedObjectLookups.js', '/static/admin/js/jquery.js', '/static/admin/js/jquery.init.js', '/static/admin/js/actions.js', '/static/admin/js/urlify.js', '/static/admin/js/prepopulate.js', '/static/zinnia/js/jquery.js', '/static/zinnia/js/jquery.bgiframe.js', '/static/zinnia/js/jquery.autocomplete.js', '/admin/zinnia/entry/autocomplete_tags/', '/static/zinnia/js/wymeditor/jquery.wymeditor.pack.js', '/static/zinnia/js/wymeditor/plugins/hovertools/jquery.wymeditor.hovertools.js', '/admin/zinnia/entry/wymeditor/']
    css = {'all': ['/static/zinnia/css/jquery.autocomplete.css']}

admin.site.register(FlatPage,FlatPageAdmin)
