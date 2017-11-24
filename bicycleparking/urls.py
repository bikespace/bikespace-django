from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/survey$', views.SurveyAnswerList.as_view()),
    url(r'^api/upload/(?P<filename>[^/]+)$', views.UploadPicture.as_view())
]
