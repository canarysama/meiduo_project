

from rest_framework import serializers

from apps.goods.models import SPU


class SpuSerializer(serializers.ModelSerializer):

    class Meta:
        model = SPU
        fields = '__all__'
