from rest_framework import serializers

class BaseSizzler(serializers.ModelSerializer):
  permissions = classmethod(lambda class_,request: request.user.is_staff)
  def get_field_names(self,*args,**kwargs):
    #if getattr(self,'_many'):
    #  return ['__unicode__',self.Meta.model._meta.pk.name]
    pk_name = self.Meta.model._meta.pk.name
    fields = super(BaseSizzler,self).get_field_names(*args,**kwargs)

    #! TODO This should maybe use pk_name once schema is in use?
    if not "pk" in fields:
      fields.append("pk")
    if not "__unicode__" in fields:
      fields.append("__unicode__")
    return fields
  def get_fields(self,*args,**kwargs):
    fields = super(BaseSizzler,self).get_fields(*args,**kwargs)
    return fields
