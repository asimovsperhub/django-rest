import jwt
from jwt import exceptions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
from django.conf import settings


class JWTQueryParamsAuthentication(BaseAuthentication):

    def authenticate(self, request):
        # 获取token并判断token的合法性
        # query_params通过url传值
        token = request.query_params.get('token')
        # 盐值
        salt = settings.SECRET_KEY
        """
        1。切割成三部分
        2。取出并解密第二部分payload：判断token是否超时
        3。验证第三部分：加盐并验证token合法性
        """
        try:
            # 从token中获取payload并校验合法性
            # jwt.decode(token,salt,True):内部集成了以上三个步骤
            payload = jwt.decode(token, salt, True)
        except  exceptions.ExpiredSignatureError:
            raise AuthenticationFailed({'code': 403, 'error': "token已经失效"})
        except  jwt.DecodeError:
            raise AuthenticationFailed({'code': 403, 'error': "token认证失败"})
        except  jwt.InvalidTokenError:
            raise AuthenticationFailed({'code': 403, 'error': '非法token'})

        """ 

            def authenticate(self, request):

            #验证请求并返回（用户，令牌）的二元组
            #Authenticate the request and return a two-tuple of (user, token).

            raise NotImplementedError(".authenticate() must be overridden.")
        """
        ##request.user=payload信息,    request.token=token信息
        return (payload, token)