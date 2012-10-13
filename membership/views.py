# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from .models import Membership

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

def join_us(request):
    values = {'memberships': Membership.objects.active()}
    return TemplateResponse(request,"membership/join-us.html",values)
