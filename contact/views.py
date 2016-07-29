from django.core.mail import mail_admins
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse

from .models import Subject, Message
from .forms import MessageForm

from PIL import Image

def contact(request):
  initial = {}
  if request.user.is_authenticated():
    initial['from_email'] = request.user.email
    initial['from_name'] = request.user.get_full_name()
  try:
    initial['contactsubject'] = Subject.objects.get(slug=request.GET.get('slug',''))
  except Subject.DoesNotExist:
    pass
  form = MessageForm(request.POST or None,initial=initial)
  if form.is_valid():
    if request.user.is_authenticated():
      form.instance.user = request.user
    form.save()
    messages.success(request,"Your message has been sent. We will respond to you as soon as possible.")
    return HttpResponseRedirect('.')
  values = {
    'form': form,
    'subjects': Subject.objects.all(),
  }
  return TemplateResponse(request,"contact.html",values)
  
def tracking_pixel(request,app,model,pk,datetime):
  try:
    datetime = datetime.replace("+"," ")
    message = Message.objects.get(pk=pk,datetime=datetime)
    message.read_count += 1
    message.save()
  except Exception,e:
    mail_admins("Bad Tracking Pixel","\n".join([app,model,pk,datetime,str(e)]))
  response = HttpResponse(content_type="image/png")
  Image.new('RGBA', (1, 1), (255,80,0,0)).save(response,"PNG")
  return response
