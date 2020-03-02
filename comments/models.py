from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User  # 引入用户模型
from mptt.models import MPTTModel, TreeForeignKey


class Comment(MPTTModel):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    text = RichTextField('内容')
    created_time = models.DateTimeField('创建时间', default=timezone.now)

       # post 为外键，关联到blog的具体某篇文章，相当于在后台数据库中多出一个post，
        # 指出这个评论是说的哪篇文章
    post = models.ForeignKey('blog.Post', verbose_name='文章', on_delete=models.CASCADE)

    # 新增 models.Model为MPTTModel
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    # 新增，记录二级评论回复给谁，str
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )

    class MPTTMeta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name


    def __str__(self):
        return '{}: {}'.format(self.name, self.text[:40])



'''
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
'''









# Create your models here.
