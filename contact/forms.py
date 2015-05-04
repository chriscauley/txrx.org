from django import forms

from .models import Message,Subject
from db.forms import PlaceholderModelForm

class MessageForm(PlaceholderModelForm):
  subject = forms.ModelChoiceField(Subject.objects,label="Please select a reason for contacting us")
  class Meta:
    model = Message
    exclude = ('user',)
