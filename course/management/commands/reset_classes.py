from django.conf import settings
from django.core.management.base import BaseCommand
from course.models import reset_classes_json
from tool.models import reset_tools_json

from drop.views.ajax import products_json

import os

class Command (BaseCommand):
  def handle(self, *args, **options):
    reset_classes_json("management command")
    reset_tools_json("management_command")
    products = products_json(None)
    f = open(os.path.join(settings.STATIC_ROOT,"products.js"),'w')
    f.write(products.content)
    f.close()
