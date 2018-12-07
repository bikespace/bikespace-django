from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/survey$', views.SurveyAnswerList.as_view()),
    url(r'^api/comments$', views.BetaCommentList.as_view()),
    url(r'^api/upload/(?P<filename>[^/]+)$', views.UploadPicture.as_view()),
    url(r'^api/pictures/(?P<filename>[^/]+)$', views.DownloadPicture.as_view()),
    url(r'^api/intersection$', views.LocationNameRequest.as_view()),
    url(r'^api/dashboarddata$', views.DashboardRequest.as_view ()),
    url(r'^sw.js', (TemplateView.as_view(template_name="bicycleparking/sw.js", content_type='application/javascript')), name='sw.js'),
    url(r'^manifest.json', (TemplateView.as_view(template_name="bicycleparking/manifest.json", content_type='application/json')), name='manifest.json'),
    url(r'^moderate_unapproved', views.submissions_to_moderate, name='moderate_unapproved'),
]
