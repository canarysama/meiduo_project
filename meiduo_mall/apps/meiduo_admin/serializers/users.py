import re
from rest_framework import  serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=('id','username','mobile','email','password')



class UserCreateSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    mobile = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate_uasername(self, value):
        if not re.match(r'[a-zA-Z0-9]{5,20}'):
            raise  serializers.ValidationError('用户名5-20')

        if User.objects.filter(username=value).count()>0:
            raise serializers.ValidationError('用户名已经存在')


        return value

    def validate_mobile(self, value):
        if not re.match(r'^1[3-9]\d{9}$',value):
            raise serializers.ValidationError('手机号错误')
        if User.objects.filter(mobile=value).count()>0:
            raise serializers.ValidationError('手机号已经存在')

        return value

    def create(self, validated_data):
        # 加密

        user = User.objects.create_user(**validated_data)

        return user









