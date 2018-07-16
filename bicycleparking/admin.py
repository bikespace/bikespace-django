from django.contrib import admin
from .models import SurveyAnswer, Approval, Event
# Register your models here.
admin.site.register(SurveyAnswer)
admin.site.register(Approval)
admin.site.register(Event)