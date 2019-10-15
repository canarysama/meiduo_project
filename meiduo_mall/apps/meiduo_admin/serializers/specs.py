
from rest_framework import  serializers

from apps.goods.models import SPUSpecification, SpecificationOption


class SpecModelSerializer(serializers.ModelSerializer):
    spu = serializers.StringRelatedField(read_only=True)
    spu_id = serializers.IntegerField()
    class Meta:
        model = SPUSpecification  # 商品规格表关联了spu表的外键spu
        fields = '__all__'

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationOption  # 商品规格表关联了spu表的外键spu
        fields = ['id','value']


class SpecOptionSerializer(serializers.ModelSerializer):
    spu = serializers.StringRelatedField(read_only=True)
    spu_id = serializers.IntegerField()
    options = OptionSerializer(read_only=True,many=True)
    class Meta:
        model = SPUSpecification  # 商品规格表关联了spu表的外键spu
        fields = '__all__'
