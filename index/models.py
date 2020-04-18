import datetime

from django.db import models


# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=20)
    pwd = models.CharField(max_length=30)
    ##允许这个字符串为空
    token = models.CharField(max_length=64, blank=True)


class Blog(models.Model):
    # 标题
    title = models.CharField(max_length=30)
    # 内容
    body = models.TextField()
    # 标签
    tag = models.CharField(max_length=20)
    # 提交时间
    post_time = models.DateTimeField(auto_now_add=True)
    # 作者
    # CASCADE：级联操作。如果外键对应的那条数据被删除了，那么这条数据也会被删除
    #阅读数,该类型的值只允许为正整数或0
    read_num=models.PositiveIntegerField(default=0)
    #评论
    comment=models.CharField('User',on_delete=models.CASCADE,max_length=200)
    #作者
    author = models.ForeignKey('User', on_delete=models.CASCADE)

    # 元数据：除了字段外的所有内容
    class Meta:
        # 排序
        ordering = ['-post_time']
        # 复数名
        verbose_name_plural = "Blogs"
    #阅读量计数
    def readnum(self):
        self.read_num += 1
        self.save(update_fields=['read_num'])


class Tag(models.Model):
    name = models.CharField(max_length=50)
