from datetime import date, timedelta

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView

from rest_framework.response import Response

from apps.goods.models import GoodsVisitCount
from apps.meiduo_admin.serializers.statistical import GoodsSerializer, GoodsModelSerializer
from apps.orders.models import OrderInfo
from apps.users.models import User


# 用户总数
class ToytalView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total = User.objects.filter(is_staff=False).count()

        return Response({
            'count': total,
            'date': date.today()
        })


# 日增用户
class DayView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        today = date.today()
        count = User.objects.filter(is_staff=False, date_joined__gte=today).count()
        return Response({

            'count': count,
            'date': today
        })


# 日活跃统计
class ActiveView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        today = date.today()

        count = User.objects.filter(is_staff=False, last_login__gte=today).count()

        return Response({

            'count': count,
            'date': today
        })

#日下单用户统计
class OrderView(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        today = date.today()

        #一个用户可能下多单 去重
        # count = OrderInfo.objects.filter(create_time__gte=today).count()
        count = User.objects.filter(orderinfo__create_time__gte=today).distinct().count()

        return Response({
            'count':count,
            'date':today
        })

#月增用户
class MonthView(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):


        today = date.today()
        countlist = list()

        for i in range(29,-1,-1):
            day_begin = today - timedelta(days = i)
            day_end = today + timedelta(days = 1)

            day_count = User.objects.filter(is_staff=False,date_joined__gte=day_begin,date_joined__lt=day_end).count()

            countlist.append({
                'date':day_begin,
                'count':day_count,

            })
        return Response(countlist)

class GoodsView(ListAPIView):
    queryset = GoodsVisitCount.objects.filter(date = date.today())
    serializer_class = GoodsSerializer