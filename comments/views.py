from blog.models import Post
from .models import Comment
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from .forms import CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url='/userprofile/login/')
def comment(request, post_pk, parent_comment_id=None):
    '''
    先获取被评论的文章，因为后面需要把评论和被评论的文章关联起来
    这里我们使用了django提供的一个快捷函数get_object_or_404
    这个函数的作用是当获取的文章(Post)存在时，则获取；否则返回404页面给用户
    '''
    post = get_object_or_404(Post, pk=post_pk)

    # django将用户提交的数据封装在request.Post中，这是一个类字典对象
    # 我们利用这些数据构造CommentForm的实例，这样就生成了一个绑定了用户提交数据的表单
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.name = request.user

            # 二级回复
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)

                # 若回复层级超过二级，则转换为二级
                comment.parent_id = parent_comment.get_root().id
                # 被回复人
                comment.reply_to = parent_comment.name
                comment.save()
                return HttpResponse('200 OK')

            comment.save()
            messages.add_message(request, messages.SUCCESS, '评论发表成功！', extra_tags='success')
            return redirect(post)
        else:
            context = {
                'post': post,
                'form': form,
            }
            messages.add_message(request, messages.ERROR, '评论发表失败！请修改表单中的错误后重新提交。', extra_tags='danger')
            return render(request, 'comments/form_error.html', context=context)

    elif request.method == 'GET':
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'post_id': post_pk,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'comments/reply.html', context)
    else:
        return HttpResponse("发表评论仅接受POST/GET请求。")

# Create your views here.
