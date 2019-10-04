from collections import OrderedDict

from django.shortcuts import render

# Create your views here.
from django.views import View

from apps.contents.models import ContentCategory
from apps.goods.models import GoodsChannel


# class IndexView(View):


    # def get(self,request):

        # categories = OrderedDict()
        # channels = GoodsChannel.objects.order_by('group_id','sequence')
        #
        # for channel in channels:
        #
        #     group_id = channel.group_id
        #
        #     if group_id not in categories:
        #         categories[group_id] = {
        #             'channels':[],
        #             'sub_cats':[],
        #         }
        #
        #
        #     cat1 = channel.category
        #
        #     #一级分类
        #     # categories[group_id]['channels'].append({
        #     #     'id':cat1.id,
        #     #     'name':cat1.name,
        #     #     'url':channel.url,
        #     #
        #     # })
        #
        #     cat1.url = channel.url
        #     categories[group_id]['channels'].append(cat1)
        #     #
        #     #
        #     # #二级分类
        #     cat2 = cat1.subs.all()
        #
        #     for cat2 in cat1.subs.all():
        #         cat2.sub_cats = []
        #         #三级分类
        #         for cat3 in cat2.subs.all():
        #             cat2.sub_cats.append(cat3)
        #
        #         categories[group_id]['sub_cats'].append(cat2)
        #
        #     context = {
        #         'categories':categories
        #
        #     }
        # return render(request, 'index.html')

from apps.contents.utlis import get_categories


class IndexView(View):
    def get(self,request):

        categories = get_categories()

        contents = {}
        ad_categories = ContentCategory.objects.all()
        for ad_cat in ad_categories:


            contents[ad_cat.key] = ad_cat.content_set.filter(status=True).order_by('sequence')

        context = {
            'categories':categories,
            'contents':contents
        }

        return render(request, 'index.html', context)