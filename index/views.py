from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from index import models
from index.createtoken.jwt_create_token import create_token

from index.models import Blog, User


# 主页
# 用户注册
class RegisterView(APIView):
    ##验证设置为空，因为settings中集成了token认证
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        # 获取用户提交的数据
        # session：request.session.get('')
        user = request.data.get('username')
        """
        def query_params(self):

            #More semantically correct name for request.GET.

            return self._request.GET
            相当于：user=request._request.GET('username')
        """
        pwd = request.data.get('password')
        # 实例化用户表
        userinfo = User()
        userinfo.username = user
        userinfo.pwd = pwd
        userinfo.save()
        return Response({'code': 200, 'successful': '注册成功'})


# 用户登陆并生成token
class LoginView(APIView):
    authentication_classes = []
    # authentication_classes = [JWTQueryParamsAuthentication]
    def post(self, request, *args, **kwargs):
        # request.data返回请求正文的解析内容
        # user = request.data.get('username')
        user = request.data.get('username')
        print(user)
        # pwd = request.data.get('password')
        pwd = request.data.get('password')
        print(pwd)
        user_object = User.objects.filter(username=user, pwd=pwd).first()
        ##如果用户名和密码不正确
        if not user_object:
            return Response({'code': 403, 'error': '用户名或密码错误'})
        # 生成token：
        token = create_token({'id': user_object.id, 'name': user_object.username})
        # 每post一次随机字符串token会变，数据库也会更新token
        user_object.save()
        # 返回给用户token
        return Response({'code': 200, 'data': token})

# token认证
class OrderView(APIView):
    ##token认证是否登陆

    def get(self, request, *args, **kwargs):
        return Response('验证成功')


# 处理写博客
class WriteView(APIView):

    def post(self, request, *args, **kwargs):
        blog = Blog()
        blog.title = request.data.get('title')
        blog.tag = request.data.get('tag')
        blog.body = request.data.get('body')
        blog.author = request.data.get('author')
        blog.save()
        return Response('上传成功')
# 用户日志
class UserlogView(APIView):

    def get(self, request, *args, **kwargs):
        id, name = request.user
        return Response({'id': id, 'name': name})


class UserView(APIView):
    pass


from index.serializers import Userserializer, Blogserializer


# Serializer类本身也是一种Field，并且可以用来表示一个对象嵌套在另一个对象中的关系。
# 也就是处理Django模型中的关系类型，一对一、多对一、多对多的字段。
@api_view(['GET'])
def userinfo(request):
    queryset = User.objects.all()
    # 嵌套的关联字段可以接收一个列表，那么应该将many = True标志传递给嵌套的序列化器,也就是多对一外键和多对多关系的处理方式
    # context参数来传递任意的附加上下文:当实例化一个HyperlinkedModelSerializer时，你必须在序列化器的上下文中包含当前的request值
    # 因为我们需要生成url字段的内容，需要request里关于请求的url路径信息(相对路径的话：可以传一个{'request': None}参数)
    serializer = Userserializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def bloginfo(request):
    queryset = Blog.objects.all()
    serializer=Blogserializer(queryset,many=True,context={'request':request})
    return Response(serializer.data)


#热门文章排名
def bloghot(request):
    #获取blog id
    nid=request.GET.get('nid')
    #获取文章
    bloghotdata=models.Blog.objects.filter(id=nid).first()
    #获取到的文章调用阅读计数的方法
    models.Blog.readnum(bloghotdata)
    #排序
    oder_byhot=models.Blog.order_by("-read_num")[0:5]
    #返回数据
    return render(request,"blog.html",locals())




