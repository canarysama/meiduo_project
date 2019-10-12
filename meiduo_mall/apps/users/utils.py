from django.contrib.auth.backends import ModelBackend
import re

from apps.users.models import User


def get_user_by_account(account):
    try:
        if re.match('^1[3-9]\d{9}$', account):
            # 手机号登录
            user = User.objects.get(mobile=account)
        else:
            # 用户名登录
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user


class UsernameMobileAuthBackend(ModelBackend):
    """自定义用户认证后端"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        重写认证方法，实现多账号登录
        :param request: 请求对象
        :param username: 用户名
        :param password: 密码
        :param kwargs: 其他参数
        :return: user
        """

        # if 'meiduo_admin' in request.path:
        #
        #     pass
        # else:
        #     pass

        if request is None:
            #后台 ：jwt调用时未传递request对象
            try:
                user = User.objects.get(username= username,is_staff=True)
            except:
                return None

            else:
                if user.check_password(password):
                    return user
                else:
                    return None

            pass
        else:
            #前台：调用式传递request对象


            user = get_user_by_account(username)

            if not user.check_password(password):
                user=None


            return user
