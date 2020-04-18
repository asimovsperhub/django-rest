import datetime
import jwt

from django.conf import settings


def create_token(payload, timeout=1):
    # 盐值
    salt = settings.SECRET_KEY
    # 固定头部格式，也可以自己改
    headers = {
        'type': 'jwt',
        'alg': 'HS256'
    }
    # 设置payload内容，目前只加一个超时时间，其他的自定义
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)
    # 生成token
    token = jwt.encode(payload=payload, key=salt, headers=headers).decode("utf-8")
    return token
