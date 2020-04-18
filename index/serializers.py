from rest_framework import serializers

# 声明序列化器
from index.models import User, Blog, Tag


# HyperlinkedModelSerializer（进一步封装了ModelSerializer类，并且自动多出了一个url字段）源码：
"""
class HyperlinkedModelSerializer(ModelSerializer):
    #核心，用于关联对象的字段类型
    serializer_related_field = HyperlinkedRelatedField
    
    #覆写了ModelSerializer中的方法，在第一个变量处发生了变化，使用了url名字。
    #与其他实例的关系是超链接，而不是主键
    #使用超链接则返回的是对应对象的url访问地址
    def get_default_field_names(self, declared_fields, model_info):
        #
        return (
            [self.url_field_name] +
            list(declared_fields) +
            list(model_info.fields) +
            list(model_info.forward_relations)
        )

    def build_nested_field(self, field_name, relation_info, nested_depth):
        #覆写了ModelSerializer中的方法，嵌套的子类依然继承的是HyperlinkedModelSerializer
        #为正向和反向关系创建嵌套字段
        class NestedSerializer(HyperlinkedModelSerializer):
            class Meta:
                model = relation_info.related_model
                depth = nested_depth - 1
                fields = '__all__'

        field_class = NestedSerializer
        field_kwargs = get_nested_relation_kwargs(relation_info)

        return field_class, field_kwargs
"""


# HyperlinkedModelSerializer类直接继承ModelSerializer类，不同之处在于它使用超链接来表示关联关系而不是主键
class Userserializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        # 可以通过将主键添加到fields选项中来显式的包含主键字段，例如下面的id：
        # 显式的设置要序列化的字段
        fields = ('url', 'id', 'username')
        # 通过在extra_kwargs中设置view_name和lookup_field中的一个或两个来重写URL字段视图名称和查询字段
        extra_kwargs = {
            # view_name对应的是urls.py中设置的路由地址，lookup_field
            'url': {'view_name': 'user', 'lookup_field': 'id'},
            # 查询字段
            'username': {'lookup_field': 'username'}
        }


class Blogserializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Blog
        fields = ('url','title', 'tag', 'body', 'post_time', 'author')
        extra_kwargs = {
            'url': {'view_name': 'blog',}
        }


class Tagserializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fiedls = ('url', 'tag')
