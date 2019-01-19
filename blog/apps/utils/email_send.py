# _*_ encoding:utf-8 _*_
__author__: '田敏伦'
__date__: '2019/1/17 0017 10:06'


from random import Random
from django.core.mail import send_mail
from users.models import EmailVerifyRecord
from blog.settings import EMAIL_FROM


def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'  # 生成所有字符和数字
    length = len(chars) - 1  # chars的长度
    randow = Random()  # 实例化随机函数
    for i in range(randomlength):
        # 随机生成长度为length的数字，这些随机数在chars里面选（加入随机数为5,那么它会在chars选择'c'），最后放在str里
        str += chars[randow.randint(0, length)]
    return str  # 返回随机数


def send_register_email(email, send_type='register'):
    code = random_str(16)
    email_record = EmailVerifyRecord()
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""
    if send_type == 'register':
        email_title = "dream网注册链接"
        email_body = "请点击下面链接激活你的账号:http://127.0.0.1:8000/active/{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])  # 会返回一个值（true / false）
        if send_status:
            pass

    if send_type == 'forget':
        email_title = "dream网找回密码链接"
        email_body = "请点击下面链接重置密码你的账号:http://127.0.0.1:8000/reset/{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])  # 会返回一个值（true / false）
        if send_status:
            pass