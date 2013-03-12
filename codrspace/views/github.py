import requests
from django.http import HttpResponseRedirect
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.template.response import TemplateResponse

from codrspace.models import Setting

class GithubAuthError(Exception):
    pass

def signin_start(request, slug=None, template_name="signin.html"):
    """Start of OAuth signin"""
    url = '%(auth_url)s?client_id=%(client_id)s&redirect_uri=%(callback_url)s'
    return HttpResponseRedirect(url%settings.GITHUB_AUTH)

def signout(request):
    if request.user.is_authenticated():
        logout(request)
    return HttpResponseRedirect(reverse(getattr(settings,'LOGOUT_REDIRECT','homepage')))


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
        values = {'err': 'Unable to get request code from Github'}
        return TemplateResponse(request, 'auth_error.html', values)

    resp = requests.post(url=settings.GITHUB_AUTH['access_token_url'],
                         data={'client_id': settings.GITHUB_AUTH['client_id'],
                               'client_secret': settings.GITHUB_AUTH['secret'],
                               'code': code})

    try:
        _validate_github_response(resp)
    except GithubAuthError, err:
        return TemplateResponse(request, 'auth_error.html', {'err': err})

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
        return HttpResponseRedirect(reverse('auth_error', args=[err]))

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
        user_defaults = {
            'username': github_user['login'],
            'is_active': True,
            'is_superuser': False,
            }

        user = User(**user_defaults)
        user.save()
        user.set_unsable_password()
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

    return HttpResponseRedirect('/')
