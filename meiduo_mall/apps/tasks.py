# from django.conf import settings
# from django.core.mail import send_mail
#
# @app.task
# def send_verify_email(self, to_email, verify_url):
#
#
#     subject = "美多商城邮箱验证"
#     html_message = '<p>尊敬的用户您好！</p>' \
#                    '<p>感谢您使用美多商城。</p>' \
#                    '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
#                    '<p><a href="%s">%s<a></p>' % (to_email, verify_url, verify_url)
#     try:
#         send_mail(subject, "", settings.EMAIL_FROM, [to_email], html_message=html_message)
#     except Exception as e:
#         logger.error(e)
#         # 有异常自动重试三次
#         raise self.retry(exc=e, max_retries=3)