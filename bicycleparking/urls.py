from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/survey$', views.SurveyAnswerList.as_view()),
    url(r'^api/comments$', views.BetaCommentList.as_view()),
    url(r'^api/moderation$', views.ModerationRequest.as_view ()),
    url(r'^api/upload/(?P<filename>[^/]+)$', views.UploadPicture.as_view()),
    url(r'^api/pictures/(?P<filename>[^/]+)$', views.DownloadPicture.as_view()),
    url(r'^api/dashboarddata$', views.DashboardRequest.as_view ()),
    url(r'^api/location$', views.LocationNameRequest.as_view()),
    url(r'^sw.js', (TemplateView.as_view(template_name="survey/sw.js", content_type='application/javascript')), name='sw.js'),
    url(r'^manifest.json', (TemplateView.as_view(template_name="survey/manifest.json", content_type='application/json')), name='manifest.json'),
    url(r'^moderate_unapproved', views.submissions_to_moderate.as_view ()),
    url( r'^login/$',auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),    
    url(r'^admin', admin.site.urls),
    url(r'^accounts', include('django.contrib.auth.urls')), # new  
]
