from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
# Create your views here.


class UserList(APIView):
    '''
    Lists all the users or create new users.
    '''
    def get(self, request):
        query_set = User.objects.all()
        serializer_class = UserSerializer(query_set, many=True)
        return Response(serializer_class.data)

    def post(self, request):
        serialized_data = UserSerializer(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data,
                            status=status.HTTP_201_CREATED)
        return Response(serialized_data.errors,
                        status=status.HTTP_400_BAD_REQUEST)
