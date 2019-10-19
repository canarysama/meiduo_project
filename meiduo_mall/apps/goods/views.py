from datetime import datetime

from django import http
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from apps.contents.utlis import get_categories
from apps.goods import models
from apps.goods.models import SKU, GoodsCategory, GoodsVisitCount
from apps.goods.utils import get_breadcrumb
from utils.response_code import RETCODE

#统计分类商品访问量

class DetailVisitView(View):
    def post(self,request,category_id):

        try:
            category = GoodsCategory.objects.get(id=category_id)
        except:
            return http.HttpResponseForbidden('不存在')

        today_str = datetime.now().strftime('%Y-%m-%d')

        today_date = datetime.strptime(today_str,'%Y-%m-%d')

        try:
            visit = GoodsVisitCount.objects.get(category=category,date= today_date )
            # visit = category.goodsvisitcount_set.get(date= today_date)
        except:
            visit = GoodsVisitCount()
        visit.count += 1
        visit.category = category
        visit.save()

        return JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})

class DetailView(View):
    """商品详情页"""

    def get(self, request, sku_id):
        """提供商品详情页"""
        # 获取当前sku的信息
        try:
            sku = models.SKU.objects.get(id=sku_id)
        except models.SKU.DoesNotExist:
            return render(request, '404.html')

        # 查询商品频道分类
        categories = get_categories()
        # 查询面包屑导航
        breadcrumb = get_breadcrumb(sku.category)

        # 构建当前商品的规格键
        sku_specs = sku.specs.order_by('spec_id')
        sku_key = []
        for spec in sku_specs:
            sku_key.append(spec.option.id)
        # 获取当前商品的所有SKU
        skus = sku.spu.sku_set.all()
        # 构建不同规格参数（选项）的sku字典
        spec_sku_map = {}
        for s in skus:
            # 获取sku的规格参数
            s_specs = s.specs.order_by('spec_id')
            # 用于形成规格参数-sku字典的键
            key = []
            for spec in s_specs:
                key.append(spec.option.id)
            # 向规格参数-sku字典添加记录
            spec_sku_map[tuple(key)] = s.id
        # 获取当前商品的规格信息
        goods_specs = sku.spu.specs.order_by('id')
        # 若当前sku的规格信息不完整，则不再继续
        if len(sku_key) < len(goods_specs):
            return
        for index, spec in enumerate(goods_specs):
            # 复制当前sku的规格键
            key = sku_key[:]
            # 该规格的选项
            spec_options = spec.options.all()
            for option in spec_options:
                # 在规格参数sku字典中查找符合当前规格的sku
                key[index] = option.id
                option.sku_id = spec_sku_map.get(tuple(key))
            spec.spec_options = spec_options

        # 渲染页面
        context = {
            'categories':categories,
            'breadcrumb':breadcrumb,
            'sku':sku,
            'specs': goods_specs,
        }
        return render(request, 'detail.html', context)

class ListView(View):
    def get(self, request, category_id, page_num):

        cat3 = GoodsCategory.objects.get(id=category_id)

        # *   1. 三级商品分类  调用 contents 封装好的代码
        categories = get_categories()

        # *   2. 面包屑组件 cat3.parent
        breadcrumb = get_breadcrumb(cat3)

        # *   3. 排序 order_by
        sort = request.GET.get('sort')

        # *    默认 价格  人气=== -create_time price -sales

        if sort == "price":
            order_field = "price"
        elif sort == "hot":
            order_field = '-sales'
        else:
            order_field = "create_time"

        skus = SKU.objects.filter(category=cat3, is_launched=True).order_by(order_field)

        # *    4. 分页器 paginator: 一页几个; 每页的内容skus; 总页数
        from django.core.paginator import Paginator
        paginator = Paginator(skus, 5)
        page_skus = paginator.page(page_num)
        total_pages = paginator.num_pages

        # *      5.热销商品

        context = {
            'categories': categories,
            'breadcrumb': breadcrumb,
            'sort': sort,  # 排序字段
            'category': cat3,  # 第三级分类
            'page_skus': page_skus,  # 分页后数据
            'total_page': total_pages,  # 总页数
            'page_num': page_num,  # 当前页码
        }

        return render(request, 'list.html', context)

class HotView(View):
    def get(self,request,category_id):
        # hot_skus = SKU.objects.filter(category_id=category_id)
        hot_skus_obj = SKU.objects.filter(category_id=category_id, is_launched=True)

        hot_skus_obj = hot_skus_obj[0:2]

        hot_skus = []
        for sku in hot_skus_obj:
            hot_skus.append({
                'id':sku.id,
                'default_image_url':sku.default_image.url,
                'name':sku.name,
                'price':sku.price,
            })
        pass
        return http.JsonResponse({'code':RETCODE.OK, 'errmsg':'OK', 'hot_skus':hot_skus})

