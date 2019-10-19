from django.conf import settings
from fdfs_client.client import Fdfs_client
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.goods.models import SKUImage
from apps.meiduo_admin.serializers.sku_image import ImageSerializer
from apps.meiduo_admin.utils.pagination import Meiduopagination


class ImageViewSet(ModelViewSet):
    pagination_class = Meiduopagination

    queryset = SKUImage.objects.all()

    serializer_class = ImageSerializer

    def create(self, request, *args, **kwargs):
        sku = request.data.get('sku')
        image = request.data.get('image')
        if not all([sku,image]):
            return Response({'detail':'数据不完整'})
        image_client = Fdfs_client(settings.FASTDFS_PATH)
        data = image_client.upload_by_buffer(image.read())
        image_name = data.get('Remote file_id')
        instance = SKUImage.objects.create(sku_id = sku,image = image_name)
        instance.save()
        ser = self.get_serializer(instance)
        return Response(ser.data,status=201)
    def update(self, request, *args, **kwargs):

        instence = ModelViewSet.get_object(self)

        sku_ID = request.data.get('sku')
        image = request.data.get('image')

        if not all([sku_ID]):
            return Response({'detail':'数据不完整'},status=400)

        if image:
            image_client = Fdfs_client(settings.FASTDFS_PATH)


            image_client.delete_file(instence.image.name)


            data = image_client.upload_by_buffer(image.read())
            instence.image = data.get('Remote file_id')

        instence.sku_id = sku_ID
        instence.save()

        serializer = self.get_serializer(instence)
        return Response(serializer.data,status=200)
    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        image_client = Fdfs_client(settings.FASTDFS_PATH)

        if instance.image.name :
            image_client.delete_file(instance.image.name)
        else:
            pass
        instance.delete()

        return Response(status=200)