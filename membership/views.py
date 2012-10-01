# Create your views here.
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

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