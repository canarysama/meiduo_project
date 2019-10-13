from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from apps.meiduo_admin.serializers.specs import SpecModelSerializer
from apps.goods.models import SPUSpecification
from apps.meiduo_admin.utils.pagination import Meiduopagination


class SpecViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = SPUSpecification.objects.all()
    serializer_class = SpecModelSerializer
    pagination_class = Meiduopagination