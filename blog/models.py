from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from django.db.models import DateTimeField


#  name是Category的一个属性，类category就相当于一个表格，
# 这样就相当于在Category的表格中建立了个一个名字为name的列，
# category的ID，Django会为我们自动创建
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# 标签s


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# 文章
class Post(models.Model):
    title = models.CharField(max_length=70)

    # 指文章正文
    body = models.TextField()  # textfield() 用来存储大段文本

    # 文章的创建时间和最后一次的修改时间，存储时间的字段用DatetimeField类型
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField(blank=True)

    # 文章摘要，blank=true是为了解决文章没有摘要的情况，因为CharField要求我们必须存入数据，否则会报错
    excerpt = models.CharField(max_length=200, blank=True)

    # 文章与标签、分类和作者author的关系
    # 我们规定一篇文章只能有一个分类，但一个分类下可有多篇文章
    # 一篇文章可以有可以有多个标签（也可以没有标签），一个标签下也可能有多篇文章
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    # 指一篇文章只能有一个作者，但一个作者可能有多篇文章
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 记录文章的浏览量
    page_views = models.PositiveIntegerField(default=0, editable=False)

    # 文章标题图
    # avatar = models.ImageField(upload_to='post/%Y%m%d/', blank=True)

    def __str__(self):
        return self.title

    # 自定义get_absolute_url(self)
    # 记得从django.urls中导入reverse函数
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.page_views += 1
        self.save(update_fields=['page_views'])



# Create your models here.
