from rest_framework import serializers
from apps.goods.models import GoodsVisitCount

class GoodsSerializer(serializers.Serializer):
    category = serializers.StringRelatedField(read_only=True)
    count = serializers.IntegerField()

class GoodsModelSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = GoodsVisitCount
        fields = ['category','count']