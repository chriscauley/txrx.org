from django import forms

from notify.models import UserSettings, METHOD_CHOICES

class NotificationForm(forms.ModelForm):
  def __init__(self,request,*args,**kwargs):
    self.request = request
    kwargs['instance'] = request.user.usermembership
    super(NotificationForm,self).__init__(request.POST or None,*args,**kwargs)
    for f in ['new_comments','my_classes','new_sessions']:
      self.fields[f].widget=forms.RadioSelect(choices=METHOD_CHOICES)
    if request.user.follow_set.all():
      self.fields['following_courses'] = forms.MultipleChoiceField(
        choices=[(f.id,unicode(f.content_object)) for f in request.user.follow_set.all()],
        widget=forms.CheckboxSelectMultiple(),
        initial=request.user.follow_set.all().values_list("id",flat=True),
        required=False,
        label="Courses you're following"
      )
  def save(self,*args,**kwargs):
    super(NotificationForm,self).save(*args,**kwargs)
    for follow in self.request.user.follow_set.all():
      if not str(follow.id) in self.request.POST.getlist('following_courses',[]):
        follow.delete()
  class Meta:
    model = UserSettings
    fields = (
      "notify_global","new_comments","my_classes","new_sessions",
    )
