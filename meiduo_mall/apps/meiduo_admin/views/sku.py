from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from apps.goods.models import SKU
from apps.meiduo_admin.serializers.sku import SKUGoodsSerializer, SKUSIMP
from apps.meiduo_admin.utils.pagination import Meiduopagination


class SKUGoodsView(ModelViewSet):
    # 指定序列化器
    serializer_class = SKUGoodsSerializer
    # 指定分页器 进行分页返回
    pagination_class = Meiduopagination

    # 重写get_queryset方法，判断是否传递keyword查询参数
    def get_queryset(self):
        # 提取keyword
        keyword = self.request.query_params.get('keyword')

        if keyword == '' or keyword is None:
            return SKU.objects.all()
        else:
            return SKU.objects.filter(name__contains=keyword)

class SKUSIMP(ListAPIView):
    queryset = SKU.objects.all()
    serializer_class = SKUSIMP