from django.http import JsonResponse
from django.utils import timezone

from .models import SMSNumber
from lablackey.decorators import auth_required

import re

parse_number = lambda n: re.sub("\D","",n)

@auth_required
def add_phone(request):
  number = parse_number(request.POST['phone_number'])
  if SMSNumber.objects.filter(number=number):
    raise NotImplementedError()
  SMSNumber.objects.create(
    number=number,
    user=request.user,
  )
  return JsonResponse({'status': 'ok'})

@auth_required
def verify_phone(request):
  try:
    number = SMSNumber.objecs.get(code=request.POST.get("verification_code",0),user=request.user)
  except SMSNumber.DoesNotExist:
    return JsonResponse({'error': 'Invalid verification code.'})
  if number.verified:
    return JsonResponse({'error': 'This number has already been verified.'})
  if number.expire < timezone.now():
    return JsonResponse({'error': 'Verification code expired'})
  number.verified = timezone.now()
  number.save()
  return JsonResonse({'status': 'ok'})
