from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.template.response import TemplateResponse

from blog.models import Post
from blog.forms import PostForm

import datetime

@staff_member_required
def drafts(request):
  return post_list(request, request.user.username, post_type='drafts')

@staff_member_required
def delete(request, pk=0, template_name="delete.html"):
  """ Delete a post """
  post = get_object_or_404(Post, pk=pk, user=request.user)
  user = get_object_or_404(get_user_model(), username=request.user.username)

  if request.method == 'POST':
    if 'delete-post' in request.POST:
      post.status = 'deleted'
      post.save()

      messages.success(request, 'Post deleted')

      return HttpResponseRedirect('post_list', args=[user.username])

  return TemplateResponse(request, template_name, {'post': post,})

@staff_member_required
def edit(request, pk=0, template_name="edit.html"):
  """ Edit a post """
  user = request.user
  post = None
  posts = Post.objects.all()
  if request.user.is_superuser:
    if pk:
      post = get_object_or_404(Post, pk=pk)
      posts = Post.objects.exclude(id=post.pk)
    posts = posts.filter(status__in=['draft', 'published'])
  else:
    if pk:
      post = get_object_or_404(Post, pk=pk, user=request.user)
      posts = Post.objects.exclude(id=post.pk)
    posts = posts.filter(user=request.user,status__in=['draft', 'published'])

  posts = posts.order_by('-pk')
  if post:
    user = post.user
  kwargs = dict(instance=post,user=user,initial={'publish_dt':datetime.datetime.now()})
  form = PostForm(request.POST or None, **kwargs)
  if request.POST and form.is_valid():
    post = form.save()
    messages.success(request,'Edited post "%s".' % post)
    return HttpResponseRedirect("/blog/admin/edit/%s/"%post.id)

  values = {
    'form': form,
    'post': post,
    'posts': posts,
    }
  return TemplateResponse(request, template_name, values)

@staff_member_required
def render_preview(request, template_name='preview.html'):
  """Ajax view for rendering preview of post"""

  post = {
    'title': request.POST.get('title',''),
    'content': request.POST.get('content',''),
  }

  return TemplateResponse(request, template_name, {'post': post,})
