from rest_framework import serializers

from apps.goods.models import GoodsCategory



class Category3Serializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"