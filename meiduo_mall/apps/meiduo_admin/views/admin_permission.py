from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import Group, Permission

from apps.meiduo_admin.serializers.admin_permission import PermissionSer, PermissionSerialzier
from apps.meiduo_admin.utils.pagination import Meiduopagination


class  PermissionView(ModelViewSet):
    serializer_class = PermissionSer
    queryset = Permission.objects.all()
    pagination_class = Meiduopagination

class GroupLIView(ListAPIView):
    serializer_class = PermissionSer
    queryset = Permission.objects.all()

    def simple(self, request):
        pers = Permission.objects.all()
        ser = PermissionSerialzier(pers, many=True)
        return Response(ser.data)