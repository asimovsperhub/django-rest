from datetime import datetime


##数据
class Comment(object):
    def __init__(self, email, content, created=None):
        self.email = email
        self.content = content
        self.created = created or datetime.now()


comment = Comment(email='1019022410@qq.com', content='wb')
#print(comment)

# 1.数据序列化

##序列化
from rest_framework import serializers, request


class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=100)
    created = serializers.DateTimeField()


ser = CommentSerializer(comment)
print(ser.data)  ##{'email': '1019022410@qq.com', 'content': 'wb', 'created': '2019-12-27T14:31:38.174192Z'}
print(type(ser.data))  # <class 'rest_framework.utils.serializer_helpers.ReturnDict'>

# 转化为成品json格式

from rest_framework.renderers import JSONRenderer

json = JSONRenderer().render(ser.data)
# 结果里的b，在Python里，这表示Bytes类型，是Python3以后的数据传输格式
print(json)  # b'{"email":"1019022410@qq.com","content":"wb","created":"2019-12-27T15:29:51.584798Z"}'
print(type(json))  # <class 'bytes'>

# 二：反序列化过程分解:从接收json数据-->数据验证--->python原生数据---->ORM层----->数据库层

import io

# 1.实际过程中并不会有先将bytes流数据转化成python原生数据这一步。
from rest_framework.parsers import JSONParser

# 将一个bytes流解析为Python原生的数据类型
stream = io.BytesIO(json)
data = JSONParser().parse(stream)
print(data)  # {'email': '1019022410@qq.com', 'content': 'wb', 'created': '2019-12-27T15:48:22.592469Z'}

# 2.将这些原生数据类型恢复到已经验证数据的字典中

##还是调用CommentSerializer函数，但是给data参数传递数据，而不是直接输入(第一)参数
ser1 = CommentSerializer(data=data)

# 数据验证
print(ser1.is_valid())  # True
# 只是从json变成了原生的Python数据类型，还不是前面定义的数据类的对象
print(ser1.validated_data)  # OrderedDict([('email', '1019022410@qq.com'), ('content', 'wb'), ('created', datetime.datetime(2019, 12, 27, 15, 38, 43, 717422, tzinfo=<UTC>))])


# 3.保存实例
# 想要返回基于验证数据的完整对象实例，我们需要实现.create()或者update()方法
class CommentSerializer1(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=100)
    created = serializers.DateTimeField()

    ##这两个方法都是继承了父类中的具体的参数形式

    # 返回验证过的数据
    def create(self, validated_data):
        #返回数据
        return Comment(**validated_data)

        #如果这里的Comment对应的是django模型的化就得通过Django-ORM将数据保存到数据库中
        # 因为这些反序列化后的数据需要交给Django-ORM模型处理
        # 所以需要将这些对象通过Django的ORM保存到数据库中
        # 返回每个对象对应的数据
        #return Comment.objects.create(**validated_data)

    # 返回数据对象（前面定义的数据类Comment中的）实例
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)

        #保存数据
        instance.save()

        return instance

#三：在视图层操作

#    视图层(views)<-------序列化器层(serializer)------->数据模型层(models)
#    序列化器层就是负责数据转换
#
#1.保存数据


#data还是用上边：python的原生数据类型

#实例化并将data数据填充

ser2=CommentSerializer1(data=data)

#数据验证
print(ser2.is_valid())     #True

print(ser2.validated_data) #OrderedDict([('email', '1019022410@qq.com'), ('content', 'wb'), ('created', datetime.datetime(2019, 12, 27, 17, 16, 59, 867570, tzinfo=<UTC>))])

#保存数据(数据验证过的)
"""
调用.save()将创建一个新实例，或更新一个现有实例，具体取决于在实例化序列化程序类时是否传递了一个现有实例：
#1.只有一个数据
ser2=CommentSerializer1(data=data)
#保存的话将创建一个新实例
ser2.save()
2。(老数据，新数据)
ser2=CommentSerializer1(comment,data=data)
#保存的话将更新已经存在的comment数据
ser2.save()
"""
# 保存实例
comment1 = ser2.save()

print(comment1)  # <__main__.Comment object at 0x102988350>

# 2.传递附加属性到sava()中，ser2.sava(owner=request)




# 在视图函数中保存实例时注入额外的数据：可以通过在.save()时添加其他关键字参数，因为序列化层中是关键字参数类型
#ser2.save(user=request.user)

# 在序列化器 .create()或.update()方法中会将视图函数中注入的参数包含在validated_data参数中


#3.重写.save()方法
#在不只需要创建新实例或更新实例的情况下，通过写.save()可实现其他功能

#添加发送邮件功能
# class   ContactForm(serializers.Serializer):
#     email=serializers.EmailField()
#     message=serializers.CharField()
#
#     def  save(self):
#         # 当我们没有写.create(）或.update()的时候，需要直接访问serializer的.validated_data属性
#         email=self.validated_data['email']
#         message=self.validated_data['message']
        #send_email(from=email,message=message)
#四。验证

#反序列化的时候要验证从前端传过来的值，是否和我们创建的对象值类型是否一致
#comment=Comment(email='1sas', content='wb')
serializer2 = CommentSerializer(data={'email': 'SASA', 'content': 'wb', 'created': '2019-12-27T15:48:22.592469Z'})
# serializer.is_valid()   #False
# serializer.errors       #字典里的每一个键都是字段名称，值是与该字段对应的错误消息的字符串列表

#内置无效数据的异常
#.is_valid()方法具有raise_exception异常标志，如果存在验证错误将会抛出一个serializers.ValidationError异常。
#默认情况下将返回HTTP 400 Bad Request响应
# serializer.is_valid(raise_exception=True)

#字段级别验证
class   BlogPostSerializer(serializers.Serializer):
    title=serializers.CharField(max_length=100)
    content=serializers.CharField()

    def validate_title(self,value):
        """
        检查博客是否和django有关
        :param value:
        :return:
        """
        if  'django' not in value.lower():
            raise serializers.ValidationError("Blog post is not  about Django")
        return value












