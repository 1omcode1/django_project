from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'created_time']  # 在数据库中评论的显示内容
    fields = ['name', 'text', 'post']  # 增加评论时的显示内容(好像没啥用，因为评论哪有自己加的)


admin.site.register(Comment, CommentAdmin)
# Register your models here.
