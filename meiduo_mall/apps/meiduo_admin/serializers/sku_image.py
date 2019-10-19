from rest_framework import serializers

from apps.goods.models import SKUImage


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKUImage
        fields = ('sku', 'image', 'id')