from django.contrib import admin

from .models import Question, UserAnswer

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
  pass

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
  raw_id_fields = ("user",)
