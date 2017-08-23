from custom_user.views import update_location
from django.conf.urls import url

urlpatterns = [
   url(r'^update-profile$', update_location)
]
