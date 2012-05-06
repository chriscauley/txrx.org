from django.conf import settings

# from membership.models as ocdir

import datetime
import urllib
import re

def clean_gkeys():
    pass

class GoogleLogin:
  def __init__ (self):
    self.google_discover_url = "https://www.google.com/accounts/o8/id"
    self.openid_ns = "http://specs.openid.net/auth/2.0"
    self.openid_ns_ext1 = "http://openid.net/srv/ax/1.0"
    self.openid_ext1_mode = "fetch_request"
    self.openid_ext1_type_email = "http://schema.openid.net/contact/email"
    self.openid_ext1_required = "email"
    self.endpoint = None
    self.claimed_id = None
    self.return_to = None
    self.realm = None
    self.assoc_handle = None
    self.require_email = False
    self.email = None
    self.op_endpoint = None
    self.response_nonce = None
    self.signed = None
    self.sig = None

  def get_login_url (self, return_url, require_email=True):
    self.get_handle()
    
    self.return_to = return_url
    self.require_email = require_email
    self.claimed_id = "http://specs.openid.net/auth/2.0/identifier_select"
    
    found = re.search("(http://.\S+?/)", return_url)
    self.realm = found.group(1)
    
    params = self.get_params("checkid_setup")
    
    url = self.end_point() + '?' + params
    
    return url
    
  def end_point (self):
    if self.op_endpoint is not None:
      return self.op_endpoint
      
    self.op_endpoint = self.get_end_point()
    return self.op_endpoint
    
  def get_params (self, mode=None):
    ret = {'openid.ns': self.openid_ns}
    
    if mode == "cancel":
      ret['openid.mode'] = "cancel"
      return ret
    
    if self.claimed_id is not None:
      ret['openid.claimed_id'] = self.claimed_id
      ret['openid.identity'] = self.claimed_id
      
    if self.return_to is not None:
      ret['openid.return_to'] = self.return_to
      
    if self.realm is not None:
      ret['openid.realm'] = self.realm
      
    if self.assoc_handle is not None:
      ret['openid.assoc_handle'] = self.assoc_handle
      
    if mode is not None:
      ret['openid.mode'] = mode
      
    if (mode == "checkid_setup" and self.require_email) or (mode == "id_res" and self.email is not None):
      ret['openid.ns.ext1'] = self.openid_ns_ext1
      ret['openid.ext1.mode'] = self.openid_ext1_mode
      ret['openid.ext1.type.email'] = self.openid_ext1_type_email
      ret['openid.ext1.required'] = self.openid_ext1_required
      if self.email is not None:
        ret['openid.ext1.value.email'] = self.email
        
    if mode == "id_res":
      ret['openid.op_endpoint'] = self.op_endpoint
      
      if self.response_nonce is not None:
        ret['openid.response_nonce'] = self.response_nonce
        
      if self.signed is not None:
        ret['openid.signed'] = self.signed
        
      if self.sig is not None:
        ret['openid.sig'] = self.sig
        
    return urllib.urlencode(ret)
    
  def get_handle (self):
    self.assoc_handle = None
    """clean_gkeys()
    
    try:
      handle = ocdir.GoogleHandle.objects.latest('ts')
      
    except:
      pass
      
    else:
      old = datetime.datetime.now() - settings.GHANDLE_EXPIRE_DAYS
      if handle.ts > old:
        self.assoc_handle = handle.handle"""
        
    if self.assoc_handle is None:
      if self.endpoint is None:
        request_url = self.get_end_point()
        
      params = {
                'openid.ns':           self.openid_ns,
                'openid.mode':         'associate',
                'openid.assoc_type':   'HMAC-SHA1',
                'openid.session_type': 'no-encryption'
               }
               
      params = urllib.urlencode(params)
      
      response = urllib.urlopen(request_url + '?%s' % params)
      found = re.search("assoc_handle:(\S+)", response.read(), re.I)
      self.assoc_handle = found.group(1)
      #h = ocdir.GoogleHandle(handle=self.assoc_handle) #!
      #h.save()
      
  def get_end_point (self):
    response = urllib.urlopen(self.google_discover_url)
    found = re.search("\<URI\>(\S+)\</URI\>", response.read(), re.I)
    return found.group(1)

