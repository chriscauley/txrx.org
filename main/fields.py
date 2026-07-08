from django.core.validators import RegexValidator
from django.db import models

class RGBColorField(models.CharField):
  """Drop-in for the dead django-colorful package: a varchar(7) '#rrggbb' field."""
  def __init__(self, *args, **kwargs):
    kwargs.setdefault('max_length', 7)
    kwargs.setdefault('validators', [RegexValidator(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')])
    super().__init__(*args, **kwargs)
