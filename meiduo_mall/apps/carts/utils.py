import json

from django_redis import get_redis_connection

from meiduo_mall.cookiesecret import CookieSecret


def merge_cart_cookie_to_redis(request, response):

    cookie_str = request.COOKIES.get('carts')

    redis_client = get_redis_connection('carts')

    if cookie_str:
        cookie_cart_dict = CookieSecret.loads(cookie_str)

        for sku_id in cookie_cart_dict:
            sku_dict = cookie_cart_dict[sku_id]
            redis_client.hset(request.user.id,sku_id,json.dumps(sku_dict))


        response.delete_cookie('carts')









