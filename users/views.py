from .serializer import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
# Create your views here.


class UserList(APIView):
    '''
    Lists all the users or create new users.
    '''
    def get(self, request):
        users = User.objects.all()
        serializer_class = UserSerializer(users)
        return Response(serializer_class)

    def post(self, request):
        pass
