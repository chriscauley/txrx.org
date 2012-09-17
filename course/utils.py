from django.contrib.auth.models import User
from django.conf import settings

def get_or_create_student(email):
    user, new = User.objects.get_or_create(email=email,defaults={'username':email})
    if new:
      user.set_password(settings.NEW_STUDENT_PASSWORD)
      user.save()
    return user
