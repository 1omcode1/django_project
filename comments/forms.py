
from django import forms
from .models import Comment


# 从model创建
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # 表明这个表单对应的数据库模型是Comment类
        fields = ['text', ]  # 指定了表单需要显示的字段
