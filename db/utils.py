def get_or_none(model,**kwargs):
  try:
    return model.objects.get(**kwargs)
  except model.DoesNotExist:
    return None
  except model.MultipleObjectsReturned:
    return model.objects.filter(**kwargs)[0]
