from rest_framework import serializers
from rest_framework.generics import ListAPIView

from apps.goods.models import GoodsCategory
from apps.meiduo_admin.serializers.category import Category3Serializer


class Cate3View(ListAPIView):
    queryset = GoodsCategory.objects.filter(subs__isnull=True)
    serializer_class = Category3Serializer









