from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'test_page', views.test_view)
    ]
