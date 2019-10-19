from django.contrib.auth.models import Group, Permission
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.meiduo_admin.serializers.admin_group import GroupSerialzier
from apps.meiduo_admin.serializers.admin_permission import PermissionSerialzier
from apps.meiduo_admin.utils.pagination import Meiduopagination


class GroupView(ModelViewSet):
    serializer_class = GroupSerialzier
    queryset = Group.objects.all()
    pagination_class = Meiduopagination

