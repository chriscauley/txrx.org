from django import forms

s = "What do you to hope accomplish at the hackerspace? What classes do you want to take? What classes are no offered that you'd like to see offered?"
e = "List any helpful skills or areas of expertise that might be relevent to the Lab. Also note if you would be interested in teaching classes in these areas."
q = "Please let us know about any questions or comment you may have about the lab, its procedures, or goals."

lr = "Reasons for joining TX/RX Labs"
lp = "Previous projects of note"
ls = "Skills you desire to learn"
le = "Skills and area of expertise"
lq = "Questions or comments"

kwargs = dict(widget=forms.Textarea,required=False)

class SurveyForm(forms.Form):
    reasons = forms.CharField(label=lr,**kwargs)
    projects = forms.CharField(label=lp,**kwargs)
    skills = forms.CharField(label=ls,help_text=s,**kwargs)
    expertise = forms.CharField(label=le,help_text=e,**kwargs)
    questions = forms.CharField(label=lq,help_text=q,**kwargs)
