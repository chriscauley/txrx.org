"""Main codrspace views"""
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.response import TemplateResponse

from codrspace.models import Post
from codrspace.forms import PostForm


@staff_member_required
def drafts(request):
    return post_list(request, request.user.username, post_type='drafts')

@staff_member_required
def delete(request, pk=0, template_name="delete.html"):
    """ Delete a post """
    post = get_object_or_404(Post, pk=pk, author=request.user)
    user = get_object_or_404(User, username=request.user.username)

    if request.method == 'POST':
        if 'delete-post' in request.POST:
            post.status = 'deleted'
            post.save()

            messages.info(request, 'Post deleted', extra_tags='alert-success')

            return HttpResponseRedirect('post_list', args=[user.username])

    return TemplateResponse(request, template_name, {'post': post,})

@staff_member_required
def edit(request, pk=0, template_name="edit.html"):
    """ Edit a post """
    post = None
    posts = Post.objects.all()
    if pk:
        post = get_object_or_404(Post, pk=pk, author=request.user)
        posts = Post.objects.exclude(id=post.pk)
    posts = posts.filter(author=request.user,status__in=['draft', 'published'])
    posts = posts.order_by('-pk')

    form = PostForm(request.POST or None, instance=post, user=request.user)    
    if request.POST and form.is_valid():
        post = form.save()
        messages.info(request,'Edited post "%s".' % post,extra_tags='alert-success')
        return HttpResponseRedirect(request.path)

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
