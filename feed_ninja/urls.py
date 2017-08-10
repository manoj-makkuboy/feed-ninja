from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'titles', views.get_title),
    url(r'articles', views.Articles.as_view()),
    ]
