from django.core.management.base import BaseCommand
from course.models import reset_classes_json

class Command (BaseCommand):
  def handle(self, *args, **options):
    reset_classes_json("management command")
