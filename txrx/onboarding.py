from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils import timezone

strftime = "%B %-d, %Y"
orientation_url = "/event/detail/105/new-member-orientation/"
orientation_link = {
  "text": "Schedule",
  "url": orientation_url
}

def active_membership(user):
  if user.paid_subscriptions:
    return { "success": True, "text": "You your %s membership is active."%user.level }
  last = user.last_subscription
  out = {
    "link": {"text": "Please sign up for a membership", "url": reverse("join_us") },
    "text": "You do not have a membership."
  }
  if last:
    out["text"] = "Your %s membership has been overdue since %s."%(last.level,last.paid_until.strftime(strftime))
  return out

def oriented(user):
  completed = user.usercriterion_set.filter(criterion_id=settings.ORIENTATION_CRITERION_ID)
  if completed:
    return {"success": True, "text": "You completed an orientation on %s."%strftime }
  for rsvp in user.rsvp_set.all():
    if getattr(rsvp.content_object,'event_id',0) == settings.ORIENTATION_ID:
      return {
        "text": "You orientation has been scheduled for %s."%rsvp.content_object.start.strftime(strftime),
        "pending": True,
        "link": {"url": orientation_url,"text": "Change" }
      }
        
  return {"text": "You have not completed an orientation.", "link": orientation_link }

def documents(user):
  messages = []
  def error(text):
    messages.append({"status": "error", "text": text})
  success = []
  if not user.headshot_url:
    error("We need an up to date photo for our records.")

  if not user.id_photo_date:
    error("We need a copy of a government issued ID.")
  else:
    success.append("ID Photo on record")
  doc_fraction = "%s/%s"%(user.done_docs,len(settings.REQUIRED_DOCUMENT_IDS))
  if user.done_docs < len(settings.REQUIRED_DOCUMENT_IDS):
    missing.append("You have signed %s required forms."%doc_fraction)
  else:
    success.append("You have signed %s required forms."%doc_fraction)
  box = "<div class='alert alert-%s'>%s</div>"
  missing = "\n".join([box%('danger',m) for m in missing])
  success = "\n".join([box%('success',m) for m in success])
  if missing:
    message = "We are missing a few required documents. Please %s as soon as possible."%orientation_link
  else:
    message = "We have all the required documents on file. Good job!"
  return not missing,"<div class='message'>%s</div>%s%s"%(message,missing,success)

def safety_training(user):
  user_criterion = user.usercriterion_set.filter(id=settings.SAFETY_CRITERION_ID,expires__isnull=True)
  now = timezone.now()
  if user_criterion:
    _t = user_criterion[0].completed.strftime(strftime)
    return {"success": True, "text": "You completed safety training on %s."%_t }
  user_criterion = user.usercriterion_set.filter(criterion_id=settings.SAFETY_CRITERION_ID,expires__gte=now)
  out = {
    "text": "You cannot enter the shop until you have completed Safety Training.",
    "link": {"text": "Enroll","url": reverse("course:detail",args=[settings.SAFETY_ID,"safety-training"])}
  }
  if user_criterion:
    _t = user_criterion[0].expires.strftime(strftime)
    out['text'] = "As a new member you must complete Safety Training by %s, or you will no longer be allowed to enter the shop."%_t
    out['pending'] = True
  return out
  _e = user.enrollment_set.filter(session__course_id=settings.SAFETY_ID,session__first_date__gte=timezone.now())
  if _e:
    _s = _e[0].session
    return {
      "text": "You are enrolled in Safety Training on %s."%_s.first_date.strftime(strftime),
      "pending": True,
      "link": {"url": _s.get_absolute_url(),"text": "Change" },
    }
