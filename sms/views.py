from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.utils import timezone

from .models import SMSNumber
from lablackey.decorators import auth_required

import re

parse_number = lambda n: re.sub("\D","",n)

@auth_required
def add_phone(request):
  number = parse_number(request.POST["phone_number"])
  try:
    smsnumber = request.user.smsnumber
  except SMSNumber.DoesNotExist:
    smsnumber = SMSNumber(user=request.user)
  if SMSNumber.objects.filter(number=number).exclude(user=request.user):
    raise NotImplementedError()
  smsnumber.number = number
  try:
    smsnumber.save()
  except IntegrityError:
    return JsonResponse({"error": "This number is being used by another user."})
  smsnumber.send_verification()
  return JsonResponse({"status": "ok"})

@auth_required
def verify_phone(request):
  try:
    print request.POST.get("verification_code",0)
    number = SMSNumber.objects.get(code=request.POST.get("verification_code",0),user=request.user)
  except SMSNumber.DoesNotExist:
    return JsonResponse({"error": "Invalid verification code."})
  if number.verified:
    return JsonResponse({"error": "This number has already been verified."})
  if number.expire < timezone.now():
    return JsonResponse({"error": "Verification code expired"})
  number.verified = timezone.now()
  number.save()
  return JsonResponse({"status": "ok", "smsnumber": number.number})

@auth_required
def delete_phone(request):
  SMSNumber.objects.filter(user=request.user).delete()
  return JsonResponse({"status": "ok"})
