#静态化首页
import os
import time

from django.conf import settings
from django.template import loader

from apps.contents.models import ContentCategory
from apps.contents.utlis import get_categories


def generate_static_index_html():
    """
    生成静态的主页html文件
    """
    print('%s: generate_static_index_html' % time.ctime())

    # 获取商品频道和分类
    categories = get_categories()

    # 广告内容
    contents = {}
    content_categories = ContentCategory.objects.all()
    for cat in content_categories:
        contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

    # 渲染模板
    context = {
        'categories': categories,
        'contents': contents
    }


    template = loader.get_template('index.html')
    # 渲染首页html字符串
    html_text = template.render(context)

    file_path = os.path.join(settings.STATICFILES_DIRS[0],'index.html')

    with open(file_path,"w") as f:
        f.write(html_text)



