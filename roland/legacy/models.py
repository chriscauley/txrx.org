# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Billingplan(models.Model):
  #yearly vs monthly, inline on membership
  id = models.IntegerField(primary_key=True,db_column="billingplanid")
  createdon = models.DateField()
  effectiveasof = models.DateField()
  endedon = models.DateField(null=True, blank=True)
  cost = models.FloatField()
  period = models.IntegerField()
  memberid = models.ForeignKey('Txrxmember', db_column='memberid')
  description = models.CharField(max_length=450, blank=True)
  descrip = models.CharField(max_length=384, blank=True)
  class Meta:
    db_table = u'billingplan'

class Financialentry(models.Model):
  id = models.IntegerField(primary_key=True,db_column="financialentryid")
  amount = models.FloatField()
  createdby = models.ForeignKey('User', db_column='createdby')
  memberid = models.ForeignKey('Txrxmember', db_column='memberid')
  paymentform = models.CharField(max_length=135, blank=True)
  entrydate = models.DateField()
  valid = models.IntegerField()
  entrytype = models.CharField(max_length=135)
  item_name = models.CharField(max_length=135, blank=True)
  payer_email = models.CharField(max_length=210, blank=True)
  payer_id = models.CharField(max_length=135, blank=True)
  payment_fee = models.FloatField(null=True, blank=True)
  txn_id = models.CharField(max_length=135, blank=True)
  txn_type = models.CharField(max_length=135, blank=True)
  postentryid = models.ForeignKey('Postentry', null=True, db_column='postentryid', blank=True)
  descrip = models.CharField(max_length=384, blank=True)
  class Meta:
    db_table = u'financialentry'

class MemberLevel(models.Model):
  id = models.IntegerField(primary_key=True,db_column="member_levelid")
  title = models.CharField(max_length=135)
  createdby = models.ForeignKey('User', db_column='createdby')
  class Meta:
    db_table = u'member_level'

class Memberbalance(models.Model):
  id = models.IntegerField(primary_key=True,db_column="memberbalanceid")
  memberid = models.ForeignKey('Txrxmember', db_column='memberid')
  updatedate = models.DateField()
  amount = models.FloatField()
  class Meta:
    db_table = u'memberbalance'

class Payment(models.Model):
  id = models.IntegerField(primary_key=True,db_column="paymentid")
  amount = models.IntegerField()
  date = models.DateField()
  createdby = models.ForeignKey('User', db_column='createdby')
  active = models.IntegerField()
  memberid = models.ForeignKey('Txrxmember', db_column='memberid')
  method = models.IntegerField()
  class Meta:
    db_table = u'payment'

class PaymentApplication(models.Model):
  id = models.IntegerField(primary_key=True,db_column="payment_applicationid")
  paymentid = models.IntegerField()
  invoiceid = models.IntegerField()
  amount = models.IntegerField()
  datestamp = models.DateField()
  active = models.IntegerField()
  createdby = models.IntegerField()
  class Meta:
    db_table = u'payment_application'

class Paypalipn(models.Model):
  id = models.IntegerField(primary_key=True,db_column="paypalipnid")
  txntype = models.CharField(max_length=135, db_column='txnType')
  txnid = models.CharField(max_length=135, db_column='txnId')
  payeremail = models.CharField(max_length=300, db_column='payerEmail')
  payerid = models.CharField(max_length=225, db_column='payerId')
  firstname = models.CharField(max_length=135, db_column='firstName', blank=True)
  lastname = models.CharField(max_length=135, db_column='lastName', blank=True)
  paymentfee = models.FloatField(db_column='paymentFee')
  paymentgross = models.FloatField(db_column='paymentGross')
  createdon = models.DateTimeField()
  processed = models.IntegerField()
  memberid = models.ForeignKey('Txrxmember', null=True, db_column='memberid', blank=True)
  class Meta:
    db_table = u'paypalIPN'

class Postentry(models.Model):
  id = models.IntegerField(primary_key=True,db_column="postentryid")
  postdate = models.DateField()
  createdby = models.ForeignKey('User', db_column='createdby')
  processedon = models.DateField()
  class Meta:
    db_table = u'postentry'

class Rfid(models.Model):
  id = models.IntegerField(primary_key=True,db_column="rfidid")
  facid = models.CharField(max_length=9, blank=True)
  cardid = models.CharField(max_length=15)
  issuedate = models.DateField()
  active = models.IntegerField()
  memberid = models.ForeignKey('Txrxmember', db_column='memberid')
  class Meta:
    db_table = u'rfid'

class Rfidpermissions(models.Model):
  id = models.IntegerField(primary_key=True,db_column="")
  rfidid = models.ForeignKey('Rfid', db_column='rfidid')
  rfidpermissiontemplateid = models.ForeignKey('Rfidpermissiontemplate',
                                               db_column='rfidpermissiontemplateid')
  class Meta:
    db_table = u'rfidpermissions'

class Rfidpermissiontemplate(models.Model):
  id = models.IntegerField(primary_key=True,db_column="rfidpermissiontemplateid")
  title = models.CharField(max_length=135)
  class Meta:
    db_table = u'rfidpermissiontemplate'

class Role(models.Model):
  id = models.IntegerField(primary_key=True,db_column="roleid")
  userid = models.ForeignKey('User', db_column='userid')
  roledefid = models.ForeignKey('Roledef', db_column='roledefid')
  class Meta:
    db_table = u'role'

class Roledef(models.Model):
  id = models.IntegerField(primary_key=True,db_column="rolddefid")
  rolename = models.CharField(max_length=135)
  class Meta:
    db_table = u'roledef'

class Txrxmember(models.Model):
  id = models.IntegerField(primary_key=True,db_column="memberid")
  firstname = models.CharField(max_length=135)
  mi = models.CharField(max_length=3, blank=True)
  lastname = models.CharField(max_length=135)
  address1 = models.CharField(max_length=135)
  address2 = models.CharField(max_length=135, blank=True)
  address3 = models.CharField(max_length=135, blank=True)
  city = models.CharField(max_length=135)
  state = models.CharField(max_length=6)
  country = models.CharField(max_length=6)
  zip_code = models.CharField(max_length=15,db_column="zip")
  primaryphone = models.CharField(max_length=21)
  primaryarea = models.CharField(max_length=9)
  email = models.CharField(max_length=135)
  joindate = models.DateField()
  member_level = models.ForeignKey('MemberLevel', db_column='member_level')
  createdby = models.ForeignKey('User', db_column='createdby')
  active = models.IntegerField()
  paypalemail = models.CharField(max_length=300, blank=True)
  deletedon = models.DateField(null=True, blank=True)
  class Meta:
    db_table = u'txrxmember'

class User(models.Model):
  id = models.IntegerField(primary_key=True,db_column="userid")
  username = models.CharField(max_length=135)
  password = models.CharField(max_length=192)
  createdon = models.DateField()
  firstname = models.CharField(max_length=135)
  mi = models.CharField(max_length=3)
  lastname = models.CharField(max_length=135)
  active = models.IntegerField()
  class Meta:
    db_table = u'user'
