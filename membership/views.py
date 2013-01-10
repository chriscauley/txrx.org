# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.flatpages.models import FlatPage
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from djpjax import pjaxtend

from .models import Membership
from .forms import UserForm, UserMembershipForm

def redirect(redirect_url):
    return HttpResponseRedirect(redirect_url)

@login_required
def login_redirect(request):
    
    #staff bounce right away
    if request.user.is_staff:
        return redirect("/admin/")
    
    elif request.user.has_perm("course.change_session"):
        return redirect("/classes/my-sessions/")
    
    else:
        return redirect("/")

@pjaxtend()
def join_us(request):
    values = {
        'memberships': Membership.objects.active(),
        'flatpage':lambda:FlatPage.objects.get(url='/join-us/'),
        }
    return TemplateResponse(request,"membership/join-us.html",values)

@login_required
def settings(request):
    user = request.user
    user_form = UserForm(request.POST or None, instance=user)
    user_membership = user.usermembership
    usermembership_form = UserMembershipForm(request.POST or None, request.FILES or None, instance=user_membership)
    if request.POST and all([user_form.is_valid(),usermembership_form.is_valid()]):
        user_form.save()
        usermembership_form.save()
        messages.success(request,'Your settings have been saved.')
        return HttpResponseRedirect(request.path)
    values = {
        'forms': [user_form, usermembership_form],
        }
    return TemplateResponse(request,'membership/settings.html',values)
