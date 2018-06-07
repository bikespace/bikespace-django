from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dashboard', views.dashboard, name='dashboard'),
    url(r'^api/survey$', views.SurveyAnswerList.as_view()),
    url(r'^api/comments$', views.BetaCommentList.as_view()),
    url(r'^api/upload/(?P<filename>[^/]+)$', views.UploadPicture.as_view()),
    url(r'^api/pictures/(?P<filename>[^/]+)$', views.DownloadPicture.as_view()),
    url(r'^api/intersection$', views.locationNames, name='locationNames'),
]
