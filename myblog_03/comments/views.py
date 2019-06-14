from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post

from .models import Comment
from .forms import CommentForm


def post_comment(request, post_pk):
    # Django 提供的一个快捷函数 get_object_or_404，
    # 这个函数的作用是当获取的文章（Post）存在时，则获取；否则返回 404 页面给用户。
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        # 我们利用这些数据构造了 CommentForm 的实例，这样 Django 的表单就生成了。
        form = CommentForm(request.POST)
        # 当调用 form.is_valid() 方法时，Django 自动帮我们检查表单的数据是否符合格式要求。
        if form.is_valid():
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
            comment = form.save(commit=False)
            # 将评论和被评论的文章关联起来。
            comment.post = post
            # 最终将评论数据保存进数据库，调用模型实例的 save 方法
            comment.save()
            # 然后重定向到 get_absolute_url 方法返回的 URL。
            return redirect(post)
        else:
            # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误。
            comment_list = post.comment_set.all()
            context = {'post': post,
                       'form': form,
                       'comment_list': comment_list
                       }
            return render(request, 'blog/detail.html', context=context)
    return redirect(post)