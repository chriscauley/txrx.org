from django import forms
from django.core.mail import send_mail

from .models import Evaluation, FIVE_CHOICES
from db.forms import PlaceholderModelForm

class RequestForm(forms.Form):
  """
  Just like a normal form but requires a request as the first argument rather than data.
  Takes GET/POST and FILES from request, so you should NOT pass these in.
  Attaches request to form for later use.

  example_form = RequestForm(request,initial={'location':'Houston'})
  user = example_form.request.user

  """
  def __init__(self,request,*args,**kwargs):
    data = request.POST or request.GET or None
    files = request.FILES or None
    super(RequestForm,self).__init__(data,files,*args,**kwargs)
    self.request = request

class EmailInstructorForm(RequestForm):
  from_address = forms.EmailField()
  subject = forms.TextInput()
  body = forms.Textarea()
  def __init__(self,session,*args,**kwargs):
    super(EmailInstructorForm,self).__init__(*args,**kwargs)
    self.session = session
  def send(self,mail_admins=True):
    """Sends email. At this point it is assumed that the form is clean and valid."""
    user = self.request.user
    extra_body = "---- RELEVANT INFORMATION ----\n"
    extra_body += "Session: %s\n"%self.session
    extra_body += "Session URL: %s\n"%self.session.get_absolute_url
    extra_body += "User: %s\n"%user.username
    if user.email != user.username and user.email != self.cleaned_data['from_address']:
      extra_body += "User email: %s"%user.email
    body = extra_body + "\n\n---- MESSAGE ----" + body
    to_addresses = [self.session.user.email]
    if mail_admins:
      to_addresses.append('chris@lablackey.com')
    send_mail(subject,body,from_address,to_addresses)

class EvaluationForm(PlaceholderModelForm):
  _kwargs = dict(choices=(('','-------'),)+FIVE_CHOICES)
  _kwargs = dict(choices=(('','-------'),)+FIVE_CHOICES)
  presentation = forms.ChoiceField(label="Instructor Presentation",help_text=Evaluation.p_ht,**_kwargs)
  content = forms.ChoiceField(label="Course Content",help_text=Evaluation.c_ht,**_kwargs)
  visuals = forms.ChoiceField(label="Handouts/Audio/Visuals",help_text=Evaluation.v_ht,**_kwargs)
  class Meta:
    model = Evaluation
    exclude = ('user','enrollment')
