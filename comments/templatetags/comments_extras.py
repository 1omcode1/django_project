
from django import template
from ..forms import CommentForm

register = template.Library()


@register.inclusion_tag('comments/inclusions/_form.html', takes_context=True)
def show_comment_form(context, post, form=None):
    if form is None:
        form = CommentForm()

    return{
            'form': form,
            'post': post,
    }


@register.inclusion_tag('comments/inclusions/_list.html', takes_context=True)
def show_comments(context, post):
    comment_list = post.comment_set.all()
    comment_count = comment_list.count()
    return{
            'comment_count': comment_count,
            'comment_list': comment_list,
            'post': post,
    }


'''
从定义可以看到，show_comment_form模板标签使用时，会接收一个post(文章Post模型的实例)作为参数，同时也可能传入一个
评论表单CommentForm的实例form，让form可以直接调用表单类的方法；如果没有接收到评论表单参数，模板标签就会新创建
一个CommentForm的实例（一个没有绑定任何数据的空表单）传给模板，否则就直接将接收到的评论表单实例直接传给模板，
这主要是为了复用已有的评论表单实例
'''
