
from rest_framework import  serializers

from apps.goods.models import SPUSpecification


class SpecModelSerializer(serializers.ModelSerializer):
    spu = serializers.StringRelatedField(read_only=True)
    spu_id = serializers.IntegerField()
    class Meta:
        model = SPUSpecification  # 商品规格表关联了spu表的外键spu
        fields = '__all__'


