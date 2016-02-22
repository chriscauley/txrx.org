from django import forms

from .models import PhotoTag, Photo

class PhotoForm(forms.ModelForm):
  class  Meta:
    fields = ('file','name')
    model = Photo

class PhotoFilterForm(forms.Form):
  search = forms.CharField(max_length=40)
  mine = forms.BooleanField()
  page = forms.IntegerField(required=False,widget=forms.HiddenInput())

class ZipForm(forms.Form):
  zip_file = forms.FileField()

class PhotoTagForm(forms.ModelForm):
  def clean_name(self):
    name = self.cleaned_data['name'].lower()
    if PhotoTag.objects.filter(name=name):
      raise forms.ValidationError("A Tag with that name already exists")
    return name
  class Meta:
    model = PhotoTag
    exclude = ()

class MultiPhotoUploadForm(forms.ModelForm):
  class Meta:
    model = Photo
    exclude = ()
