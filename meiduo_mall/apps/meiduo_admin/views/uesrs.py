

from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination

from apps.meiduo_admin.serializers.users import UserSerializer, UserCreateSerializer
from apps.meiduo_admin.utils.pagination import Meiduopagination
from apps.users.models import User






class UserView(ListCreateAPIView):
    # queryset =  User.objects.filter(is_staff=False)

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        return User.objects.filter(is_staff=False,username__contains=keyword)


    # serializer_class = UserSerializer
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        else:
            return UserCreateSerializer

    pagination_class = Meiduopagination

