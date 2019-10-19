from django.conf.urls import url
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token

from apps.meiduo_admin.views.admin_group import GroupView
from apps.meiduo_admin.views.admin_permission import PermissionView, GroupLIView
from apps.meiduo_admin.views.category import Cate3View
from apps.meiduo_admin.views.orders import OrderSet
from apps.meiduo_admin.views.sku import SKUGoodsView
from apps.meiduo_admin.views.sku import SKUSIMP
from apps.meiduo_admin.views.sku_image import ImageViewSet
from .views import statistical
from .views import specs
from .views import spu
from apps.meiduo_admin.views.uesrs import UserView
from apps.goods import views
from rest_framework.routers import SimpleRouter, DefaultRouter

urlpatterns = [
    url(r'^authorizations/$', obtain_jwt_token),

    url(r'^statistical/total_count/$', statistical.ToytalView.as_view()),

    url(r'^statistical/day_increment/$', statistical.DayView.as_view()),

    url(r'^statistical/day_active/$', statistical.ActiveView.as_view()),

    url(r'^statistical/day_orders/$', statistical.OrderView.as_view()),

    url(r'^statistical/month_increment/$', statistical.MonthView.as_view()),


    url(r'^statistical/goods_day_views/$', statistical.GoodsView.as_view()),

    url(r'^users/$', UserView.as_view()),

    url(r'^goods/simple/$', spu.SpuSimleView.as_view()),

    url(r'^goods/(?P<pk>\d+)/specs/$', specs.SpecOpTIONView.as_view()),

    url(r'^skus/categories/$', Cate3View.as_view()),

    url(r'^skus/simple/$', SKUSIMP.as_view()),
    url(r'^permission/simple/$', GroupLIView.as_view()),



]

ro  = SimpleRouter()
ro.register('goods/specs',specs.SpecViewSet,base_name='specs')

urlpatterns += ro.urls

router = DefaultRouter()
router.register('skus/images',ImageViewSet,base_name='images')
router.register('skus', SKUGoodsView, base_name='skus')
router.register('orders', OrderSet, base_name='orders')
router.register('permission/perms', PermissionView, base_name='PermissionView')
router.register('permission/groups', GroupView, base_name='PermissionView')
urlpatterns += router.urls
