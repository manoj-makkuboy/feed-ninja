from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'get_title', views.get_title)
    ]
