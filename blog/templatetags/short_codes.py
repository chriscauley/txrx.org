import requests
import mimetypes
import re
import os
import markdown
from hashlib import md5

from django import template
from django.template.defaultfilters import striptags
from django.utils.safestring import mark_safe
from settings import MEDIA_ROOT

from .syntax_color import _colorize_table

import json

register = template.Library()

urlfinder = re.compile('^(http:\/\/\S+)')
urlfinder2 = re.compile('\s(http:\/\/\S+)')

@register.filter
def explosivo(value,safe_mode=False):
  """
  Search text for any references to supported short codes and explode them
  """
  value = value or ""

  # Round-robin through all functions as if they are filter methods so we
  # don't have to update some silly list of available ones when they are
  # added
  import sys
  import types
  module = sys.modules[__name__]
  all_replacements = []

  # get the replacement values and content with replacement hashes
  for name, var in vars(module).items():
    if type(var) == types.FunctionType and name.startswith('filter_'):
      replacements, value, match = var(value)
      if match:
        all_replacements.extend(replacements)

  # find urls, convert to links

  # convert to markdown
  value = markdown.markdown(value,safe_mode=safe_mode)

  #value = urlfinder.sub(r'<a href="\1">\1</a>', value)
  #value = urlfinder2.sub(r' <a href="\1">\1</a>', value)

  # replace the hash values with the replacement values
  for r in all_replacements:
    _hash, text = r
    value = value.replace(_hash, text)

  return mark_safe(value)

@register.filter
def public_explosivo(value):
  return explosivo(value,safe_mode='escape')

@register.filter
def implosivo(value):
  # like explosivo but it renders the page as plain text
  return striptags(explosivo(value))

def filter_jsfiddle(value):
  """Used to insert fiddle iframe. format: [jsfiddle "username/id" opt1=val1,opt2=val2...]"""
  replacements = []
  pattern = re.compile('\\[jsfiddle (?P<values>[^\\]]*)\\]', re.I | re.S | re.M)

  if len(re.findall(pattern, value)) == 0:
    return (replacements, value, None,)

  shortcodes = re.finditer(pattern, value)

  for shortcode in shortcodes:
    values = shortcode.group('values').split(' ')
    code = values[0]
    base_url = "http://jsfiddle.net/%(code)s/embedded/%(tabs)s/"
    options = {
      'code': code,
      'width': 640,
      'height': 400,
      'tabs': 'result,js,resources,html,css',
      'style': '',
      }
    for k,v in [i.split('=') for i in values[1:]]:
      options[k] = v
    if options['tabs'] == 'result':
      base_url = 'http://fiddle.jshell.net/%(code)s/show/'
    options['url'] = base_url%options
    tag = '<iframe src="%(url)s" width="%(width)s" height="%(height)s" style="%(style)s"></iframe>'%options
    replacements.append(['[jsfiddle %s]'%(' '.join(values)),tag])

  return (replacements, value, True,)
  

def filter_inline(value):
  replacements = []
  pattern = re.compile('\\[code(\\s+lang=\"(?P<lang>[\\w]+)\")*\\](?P<code>.*?)\\[/code\\]', re.I | re.S | re.M)

  if len(re.findall(pattern, value)) == 0:
    return (replacements, value, None,)

  inlines = re.finditer(pattern, value)

  for inline_code in inlines:
    try:
      lang = inline_code.group('lang')
    except IndexError:
      lang = None

    text = _colorize_table(inline_code.group('code'), lang=lang)
    text_hash = md5(text.encode('utf-8')).hexdigest()

    replacements.append([text_hash, text])
    value = re.sub(pattern, text_hash, value, count=1)

  return (replacements, value, True,)


def filter_gist(value):
  gist_base_url = 'https://api.github.com/gists/'
  replacements = []
  pattern = re.compile('\[gist (\d+) *\]', flags=re.IGNORECASE)

  ids = re.findall(pattern, value)
  if not len(ids):
    return (replacements, value, None,)

  for gist_id in ids:
    gist_text = ""
    lang = None
    resp = requests.get('%s%d' % (gist_base_url, int(gist_id)))

    if resp.status_code != 200:
      return (replacements, value, None,)

    content = json.loads(resp.content)

    # Go through all files in gist and smash 'em together
    for name in content['files']:
      _file = content['files'][name]

      # try and get the language of the file either
      # by passing filename or by passing the language
      # specified
      if 'filename' in _file:
        lang = _file['filename']
      elif 'language' in _file:
        lang= _file['language']

      gist_text += "%s" % (
        _colorize_table(_file['content'], lang=lang))

    if content['comments'] > 0:
      gist_text += '<hr><p class="github_convo">Join the conversation on ' + \
              '<a href="%s#comments">github</a> (%d comments)</p>' % (
                content['html_url'], content['comments'])

    text_hash = md5(gist_text.encode('utf-8')).hexdigest()

    replacements.append([text_hash, gist_text])
    value = re.sub(pattern, text_hash, value, count=1)

  return (replacements, value, True,)

def filter_upload(value):
  replacements = []
  pattern = re.compile('\[local (\S+) *\]', flags=re.IGNORECASE)

  files = re.findall(pattern, value)
  if not len(files):
    return (replacements, value, None,)

  for file_name in files:
    colorize = True
    file_path = os.path.join(MEDIA_ROOT, file_name)
    (file_type, encoding) = mimetypes.guess_type(file_path)

    if file_type is None:
      colorize = False

    # FIXME: Can we trust the 'guessed' mimetype?
    if file_type in ['application', 'text']:
      colorize = False

    # FIXME: Limit to 1MB right now
    try:
      f = open(file_path)
      text = f.read(1048576)
      f.close()
    except IOError:
      colorize = False

    if colorize:
      text = _colorize_table(text, lang=file_name)
      text_hash = md5(text.encode('utf-8')).hexdigest()
    else:
      text = '[local %s]' % file_name
      text_hash = md5(text.encode('utf-8')).hexdigest()

    replacements.append([text_hash, text])
    value = re.sub(pattern, text_hash, value, count=1)

  return (replacements, value, True,)
