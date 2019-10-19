from rest_framework import serializers
from django.contrib.auth.models import Permission,Group,User
from django.db import migrations,models


class PurviewSer(serializers.ModelSerializer,migrations.Migration):
    class Meta:
        model = migrations.Migration
        fields = "__all__"