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
    
        """
        if request.user.has_perm("timecard.add_entry"):
            return redirect("/timecard/my-time/")
        else:
            return redirect("/")
        """
        
    else:
        return redirect("/")