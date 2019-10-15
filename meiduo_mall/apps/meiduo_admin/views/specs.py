from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from apps.meiduo_admin.serializers.specs import SpecModelSerializer, SpecOptionSerializer
from apps.goods.models import SPUSpecification
from apps.meiduo_admin.utils.pagination import Meiduopagination


class SpecViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = SPUSpecification.objects.all()
    serializer_class = SpecModelSerializer
    pagination_class = Meiduopagination

class SpecOpTIONView(ListAPIView):
    def get_queryset(self):
        spu_id = self.kwargs.get('pk')
        return SPUSpecification.objects.filter(spu_id=spu_id)


    serializer_class = SpecOptionSerializer