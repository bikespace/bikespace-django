from django.contrib import admin
from .models import SurveyAnswer, Picture, Event, Approval
from django.utils.html import format_html
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

admin.site.register(SurveyAnswer)
admin.site.register(Approval)
admin.site.register(Event)


@admin.register(Picture)
class Pictures(admin.ModelAdmin):

    def get_queryset(self, request):
        """Only show unapproved pictures"""
        approved_event_ids = Approval.objects.values_list('approved')
        unapproved_pictures = Picture.objects.exclude(answer_id__in=approved_event_ids)
        return unapproved_pictures

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<picture_id>.+)/approve/$',
                self.admin_site.admin_view(self.picture_approve),
                name='picture-approve',
            ),
        ]
        return custom_urls + urls

    def picture_approve(self, request, picture_id):
        picture = Picture.objects.get(id=picture_id)
        surveyanswer = picture.answer
        event = Event.objects.get(answer=surveyanswer)
        Approval.objects.get_or_create(approved=event)
        return HttpResponseRedirect(reverse('admin:bicycleparking_picture_changelist'))

    def image_tag(self, obj):
        return format_html(
            '<a href="https://s3.amazonaws.com/bikeparking/{}"><img src="https://s3.amazonaws.com/bikeparking/{}" style="max-width: 400px; max-height: 400px"/></a>'.format(
                obj.photo_uri, obj.photo_uri))

    def approve(self, obj):
        return format_html(
            '<a class="button" href="{}">Approve</a>&nbsp;'.format(reverse('admin:picture-approve', args=[obj.id])))

    list_display = ('image_tag', 'approve',)
    fields = ('image_tag', 'approve',)
    readonly_fields = ('image_tag',)
