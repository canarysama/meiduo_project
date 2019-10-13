from rest_framework.generics import ListAPIView

from apps.goods.models import SPU
from apps.meiduo_admin.serializers.spu import SpuSerializer


class SpuSimleView(ListAPIView):
    queryset = SPU.objects.all()
    serializer_class = SpuSerializer

