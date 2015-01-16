from django import forms

from .models import ContactMessage,ContactSubject
from db.forms import PlaceholderModelForm

class ContactMessageForm(PlaceholderModelForm):
  contactsubject = forms.ModelChoiceField(ContactSubject.objects,label="Please select a reason for contacting us")
  class Meta:
    model = ContactMessage
    exclude = ('user',)
