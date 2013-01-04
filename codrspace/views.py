"""Main codrspace views"""
import requests
from datetime import datetime

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.core.cache import cache
from django.core.paginator import Paginator
from django.template.response import TemplateResponse

from tagging.models import Tag

from codrspace.models import Post, Profile, Photo, Setting
from codrspace.forms import PostForm, PhotoForm, SettingForm, FeedBackForm, PhotoFilterForm

class GithubAuthError(Exception):
    pass


def index(request, template_name="home.html"):
    return render(request, template_name)


def post_detail(request, username, slug, template_name="post_detail.html"):
    user = get_object_or_404(User, username=username)

    post = get_object_or_404(
        Post,
        author=user,
        slug=slug,)

    try:
        user_settings = Setting.objects.get(user=user)
    except:
        user_settings = None

    if post.status == 'draft':
        if post.author != request.user:
            raise Http404

    return render(request, template_name, {
        'username': username,
        'post': post,
        'meta': user.profile.get_meta(),
        'user_settings': user_settings
    })


def post_list(request, username, post_type='published',
              template_name="post_list.html"):
    user = get_object_or_404(User, username=username)

    try:
        user_settings = Setting.objects.get(user=user)
    except:
        user_settings = None

    if post_type == 'published':
        post_type = 'posts'
        status_query = Q(status="published")
    else:
        post_type = 'drafts'
        status_query = Q(status="draft")

    posts = Post.objects.filter(
        status_query,
        Q(publish_dt__lte=datetime.now()) | Q(publish_dt=None),
        author=user,
    )
    posts = posts.order_by('-publish_dt')

    return render(request, template_name, {
        'username': username,
        'posts': posts,
        'post_type': post_type,
        'meta': user.profile.get_meta(),
        'user_settings': user_settings
    })


@staff_member_required
def drafts(request):
    return post_list(request, request.user.username, post_type='drafts')


@staff_member_required
def add(request, template_name="edit.html"):
    """ Add a post """

    posts = Post.objects.filter(
        author=request.user,
        status__in=['draft', 'published']
    ).order_by('-pk')

    if request.method == "POST":

        # post
        form = PostForm(request.POST, user=request.user)
        if 'submit_post' in request.POST and form.is_valid():
            form.author = request.user
            post = form.save()

            if post.status == 'published' and not post.publish_dt:
                post.publish_dt = datetime.now()
            post.save()
            messages.info(
                request,
                'Added post "%s".' % post,
                extra_tags='alert-success')
            return redirect('edit', pk=post.pk)

    else:
        form = PostForm(user=request.user,initial={'publish_dt':datetime.now()})

    return render(request, template_name, {
        'form': form,
        'posts': posts,
    })


@staff_member_required
def user_settings(request, template_name="settings.html"):
    """ Add/Edit a setting """

    user = get_object_or_404(User, username=request.user.username)

    try:
        settings = Setting.objects.get(user=user)
    except Setting.DoesNotExist:
        settings = None

    form = SettingForm(instance=settings)

    if request.method == 'POST':
        form = SettingForm(request.POST, instance=settings)
        if form.is_valid():
            msg = "Edited settings successfully."
            messages.info(request, msg, extra_tags='alert-success')
            settings = form.save(commit=False)
            settings.user = user
            settings.save()

            # clear settings cache
            cache_key = '%s_user_settings' % user.pk
            cache.set(cache_key, None)

    return render(request, template_name, {
        'form': form,
    })


@staff_member_required
def api_settings(request, template_name="api_settings.html"):
    """ View API settings """

    from tastypie.models import ApiKey
    api_key = get_object_or_404(ApiKey, user=request.user)

    return render(request, template_name, {
        'api_key': api_key,
    })


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

            return redirect(reverse('post_list', args=[user.username]))

    return render(request, template_name, {
        'post': post,
    })


@staff_member_required
def edit(request, pk=0, template_name="edit.html"):
    """ Edit a post """
    post = get_object_or_404(Post, pk=pk, author=request.user)
    posts = Post.objects.exclude(id=post.pk)
    posts = posts.filter(author=request.user,status__in=['draft', 'published'])
    posts = posts.order_by('-pk')

    form = PostForm(request.POST or None, instance=post, user=request.user)    
    if request.POST and form.is_valid():
        form.save()
        messages.info(request,'Edited post "%s".' % post,extra_tags='alert-success')
        return HttpResponseRedirect(request.path)

    return render(request, template_name, {
        'form': form,
        'post': post,
        'posts': posts,
    })


def signin_start(request, slug=None, template_name="signin.html"):
    """Start of OAuth signin"""

    return redirect('%s?client_id=%s&redirect_uri=%s' % (
                    settings.GITHUB_AUTH['auth_url'],
                    settings.GITHUB_AUTH['client_id'],
                    settings.GITHUB_AUTH['callback_url']))


def signout(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect(reverse(getattr(settings,'LOGOUT_REDIRECT','homepage')))


def _validate_github_response(resp):
    """Raise exception if given response has error"""

    if getattr(resp,'error',None) is not None:
        raise GithubAuthError('Could not communicate with Github API (%s)' % (
                                                            resp.error.reason))

    if resp.status_code != 200 or 'error' in resp.content:
        raise GithubAuthError('code: %u content: %s' % (resp.status_code,
                                                  resp.content))


def _parse_github_access_token(content):
    """Super hackish way of parsing github access token from request"""
    # FIXME: Awful parsing w/ lots of assumptions
    # String looks like this currently
    # access_token=1c21852a9f19b685d6f67f4409b5b4980a0c9d4f&token_type=bearer
    return content.split('&')[0].split('=')[1]


def signin_callback(request, slug=None, template_name="base.html"):
    """Callback from Github OAuth"""

    try:
        code = request.GET['code']
    except KeyError:
        return render(request, 'auth_error.html', dictionary={
                            'err': 'Unable to get request code from Github'})

    resp = requests.post(url=settings.GITHUB_AUTH['access_token_url'],
                         data={'client_id': settings.GITHUB_AUTH['client_id'],
                               'client_secret': settings.GITHUB_AUTH['secret'],
                               'code': code})

    try:
        _validate_github_response(resp)
    except GithubAuthError, err:
        return render(request, 'auth_error.html', dictionary={'err': err})

    token = _parse_github_access_token(resp.content)

    # Don't use token unless running in production b/c mocked service won't
    # know a valid token
    user_url = settings.GITHUB_AUTH['user_url']

    if not settings.GITHUB_AUTH['debug']:
        user_url = '%s?access_token=%s' % (user_url, token)

    resp = requests.get(user_url)

    try:
        _validate_github_response(resp)
    except GithubAuthError, err:
        return redirect(reverse('auth_error', args=[err]))

    github_user = simplejson.loads(resp.content)

    user = None

    try:
        user = User.objects.get(username=github_user['login'])
    except User.DoesNotExist:
        try:
            user = User.objects.get(email=github_user['email'])
        except User.DoesNotExist:
            pass

    if not user:
        password = User.objects.make_random_password()
        user_defaults = {
            'username': github_user['login'],
            'is_active': True,
            'is_superuser': False,
            'password': password}

        user = User(**user_defaults)
        user.save()

    # Get/Create the user profile
    try:
        profile = user.get_profile()
    except Profile.DoesNotExist:
        profile = Profile(
            git_access_token=token,
            user=user,
            meta=resp.content
        )

    # update meta information and token
    profile.git_access_token = token
    profile.meta = resp.content
    profile.save()

    # Create settings for user
    try:
        user_settings = Setting.objects.get(user=user)
    except Setting.DoesNotExist:
        s = Setting()
        s.user = user
        s.timezone = "US/Central"
        s.save()

    # Fake auth b/c github already verified them and we aren't using our
    # own #passwords...yet?
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)

    return redirect('/')


@login_required
def feedback(request, template_name='feedback.html'):
    """ Send Feed back """
    from django.core.mail import mail_admins
    user = get_object_or_404(User, username=request.user.username)

    form = FeedBackForm(initial={'email': user.email})

    if request.method == 'POST':
        form = FeedBackForm(request.POST)
        if form.is_valid():
            msg = "Thanks for send us feedback. We hope to make the product better."
            messages.info(request, msg, extra_tags='alert-success')

            print dir(form)
            subject = 'Codrspace feedback from %s' % user.username
            message = '%s (%s), %s' % (
                request.user.username,
                form.cleaned_data['email'],
                form.cleaned_data['comments'],
            )

            mail_admins(subject, message, fail_silently=False)

    return render(request, template_name, {
        'form': form,
    })


@staff_member_required
def render_preview(request, template_name='preview.html'):
    """Ajax view for rendering preview of post"""

    # make a mock post
    post = {
        'title': '',
        'content': ''
    }

    if request.method == 'POST':
        if 'title' in request.POST:
            post['title'] = request.POST['title']
        if 'content' in request.POST:
            post['content'] = request.POST['content']

    return render(request, template_name, {
        'post': post,
    })


def insert_photo(request):
    photos = Photo.objects.all()
    if not request.GET or request.GET.get('mine',False):
        photos = photos.filter(user=request.user)
    form = PhotoFilterForm(request.GET or None,initial={'mine':True})
    paginator = None
    if photos:
        paginator = Paginator(photos,8)
        photos = paginator.page(request.GET.get('page',1))
    values = {
        "paginator": paginator,
        "photos": photos,
        "form": form,
        }
    return TemplateResponse(request,"codrspace/insert_photo.html",values)

def add_photo(request):
    photo = None
    form = PhotoForm(request.POST or None,request.FILES or None)
    if request.POST and form.is_valid():
        photo = form.save()
        photo.user = request.user
        photo.save()
        # Not redirecting because we're going to close modal using javascript
    values = {
        'photo': photo,
        'form': form,
        }
    return TemplateResponse(request,"codrspace/add_photo.html",values)

def posts_by_tag(request,name):
    tag = get_object_or_404(Tag,name=name)
    items = tag.items.filter(content_type__app_label="codrspace",content_type__name="post",object_id__isnull=False)
    posts = [item.object for item in items]
    values = {
        "posts": posts,
        "tag": tag,
        }
    return TemplateResponse(request,"codrspace/posts_by_tag.html",values)
