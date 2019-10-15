from rest_framework import serializers
from celery_tasks.detail.tasks import generate_task

from apps.goods.models import SKUSpecification, SKU
from django.db import transaction

# class SKUSpecificationSerialzier(serializers.ModelSerializer):
#     """
#     SKU规格表序列化器
#     """
#     spec_id = serializers.IntegerField(read_only=True)
#     option_id = serializers.IntegerField(read_only=True)
#
#     class Meta:
#         model = SKUSpecification
#         fields = ("spec_id", 'option_id')

class SKUSpecificationSerialzier(serializers.Serializer):
    """
    SKU规格表序列化器
    """
    spec_id = serializers.IntegerField()
    option_id = serializers.IntegerField()


class SKUGoodsSerializer(serializers.ModelSerializer):
    """
    # 获取sku表信息的序列化器
    # """
    specs = SKUSpecificationSerialzier(many=True)
    # 指定分类信息
    category_id = serializers.IntegerField()
    # 关联嵌套返回
    category = serializers.StringRelatedField(read_only=True)
    # 指定所关联的spu表信息
    spu_id = serializers.IntegerField()
    # 关联嵌套返回
    spu = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SKU
        fields = '__all__'

    def create(self, validated_data):

        specs = validated_data.pop('specs')

        with transaction.atomic():

            sid = transaction.savepoint()
            try:
                sku = super().create(validated_data)

                for item in specs:
                    item['sku_id'] = sku.id
                    SKUSpecification.objects.create(

                       **item

                    )
            except:
                transaction.savepoint_rollback(sid)
                raise serializers.ValidationError('创建sku失败')
            else:

                transaction.savepoint_commit(sid)

                #异步生成静态文件
                generate_task.delay(sku.id)

                return sku

    def update(self, instance, validated_data):
        # 1.取出specs数据
        specs = validated_data.pop('specs')

        with transaction.atomic():
            sid = transaction.savepoint()
            try:
                # 2.调用父类方法修改实例
                instance = super().update(instance, validated_data)

                # 3.修改规格及选项
                # 3.1删除所有规格
                SKUSpecification.objects.filter(sku_id=instance.id).delete()

                # 3.2遍历，创建规格
                for item in specs:
                    item['sku_id'] = instance.id
                    SKUSpecification.objects.create(**item)
            except:
                transaction.savepoint_rollback(sid)
                raise serializers.ValidationError('修改sku失败')
            else:
                transaction.savepoint_commit(sid)

                generate_task.delay(instance.id)

                return instance