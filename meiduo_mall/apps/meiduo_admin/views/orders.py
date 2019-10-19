from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.meiduo_admin.serializers.orders import OrderSeriazlier
from apps.meiduo_admin.utils.pagination import Meiduopagination
from apps.orders.models import OrderInfo
from rest_framework.decorators import action

class OrderSet(ReadOnlyModelViewSet):
    # queryset = OrderInfo.objects.order_by('-create_time')
    serializer_class = OrderSeriazlier
    pagination_class = Meiduopagination

    def get_queryset(self):
        key = self.request.query_params.get('keyword')

        queryset = OrderInfo.objects

        if key:
            queryset = queryset.filter(order_id=key)

        queryset = queryset.order_by('-create_time')
        return queryset

    @action(methods=['PUT'],detail=True)
    def status(self,request,*args,**kwargs):
        instance = self.get_object()

        instance.states = 3

        instance.save()

        return Response({
            'order_id':instance.order_id ,
            'states':instance.states

        },status=201)

