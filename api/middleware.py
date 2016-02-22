from django.conf import settings
from django.core.urlresolvers import reverse

from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

social_complete = '%s:complete'%getattr(settings,'SOCIAL_AUTH_URL_NAMESPACE','social')

"""authentication_paths = [
  reverse('auth_login'),
  reverse(social_complete,args=['github']),
  reverse(social_complete,args=['google-oauth2']),
]"""
  
class JWTMiddleware(object):
  def process_request(self, request):
    self.user_in = request.user.is_authenticated()
  def process_response(self, request, response):
    if not getattr(self,'user_in',False) and hasattr(request,"user") and request.user.is_authenticated():
      # user just logged in but doesn't have a web token
      payload = jwt_payload_handler(request.user)
      response.set_cookie('JWT-Token', jwt_encode_handler(payload))
    return response
