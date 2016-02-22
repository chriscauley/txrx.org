from django.core.management.base import BaseCommand
from course.models import reset_classes_json
from tool.models import reset_tools_json

class Command (BaseCommand):
  def handle(self, *args, **options):
    reset_classes_json("management command")
    reset_tools_json("management_command")
