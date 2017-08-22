from django.shortcuts import render
from rest_framework.decorators import api_view
from custom_user.serializers import CustomUserSerializer
#from custom_user.models import CustomUser
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@api_view(['GET','POST'])
def update_location(request):
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.id)
        user.customuser.location = request.data['location']
        serialized_obj = CustomUserSerializer(user, data=request.data)
        return Response("Done")
