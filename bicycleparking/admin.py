from django.contrib import admin
from .models import SurveyAnswer, Approval, Event, Picture
# Register your models here.
admin.site.register(SurveyAnswer)
admin.site.register(Approval)
admin.site.register(Event)
admin.site.register (Picture)