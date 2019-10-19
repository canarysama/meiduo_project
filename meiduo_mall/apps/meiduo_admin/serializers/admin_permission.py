from rest_framework import serializers
from django.contrib.auth.models import Permission




class PermissionSer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"

class PermissionSerialzier(serializers.ModelSerializer):
    """
    用户权限表序列化器
    """

    class Meta:
        model = Permission
        fields = "__all__"