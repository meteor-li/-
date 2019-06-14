from django.shortcuts import render,get_object_or_404
import markdown
# Q 对象用于包装查询表达式，其作用是为了提供复杂的查询逻辑
from django.db.models import Q
from .models import Category,Tag,Post
from comments.forms import CommentForm
# 发送邮件
import smtplib
from email.mime.text import MIMEText
# 博客主页
def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    '''
    order_by 方法对这个返回进行排序。排序依据的字段是 created_time
    '''
    return render(request, 'blog/index.html', context={'post_list': post_list})
# 文章主要内容
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()# 阅读量+1
    # post.body = markdown.markdown(post.body,
    #                               extensions=[
    #                                   'markdown.extensions.extra',
    #                                   'markdown.extensions.codehilite',
    #                                   'markdown.extensions.toc',
    #                               ])
    form = CommentForm()
    # 获取全部评论
    comment_list = post.comment_set.all()

    # 将文章、表单、以及文章下的评论列表传值
    context = {'post': post,
               'form': form,
               'comment_list': comment_list
               }
    return render(request, 'blog/detail.html', context=context)
# 发布时间页
def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
# 文章分类页
def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
# 联系
def contact(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        # 邮件服务器
        mail_server = 'smtp.qq.com'
        # 用户名
        mail_username = '1337983798@qq.com'
        # 密码，通过环境变量获取，可以避免隐私信息的暴露
        # 或授权码，QQ邮箱需要使用授权码
        mail_password = 'eqaoqhrtffngigia'
        # 邮件内容
        content = 'QQ:1337983798' \
                  '微信：18438603979'
        # 创建用于发送的邮件消息对象
        # 参数1：邮件内容
        # 参数2：内容类型，plain表示普通文本，html表示网页
        message = MIMEText(content)
        # 设置主题
        message['Subject'] = '联系方式邮件'
        # 设置发送者
        message['From'] = mail_username

        # 创建用于发送邮件的对象
        # SMTP：邮件不加密，端口25
        # SMTP_SSL：邮件加密传输，端口465，QQ邮箱必须使用加密
        mail = smtplib.SMTP(mail_server)
        # 身份认证
        mail.login(mail_username, mail_password)
        # 发送给谁
        to = user
        # 发送邮件
        mail.sendmail(mail_username, to, message.as_string())
        # 结束
        mail.quit()
        return render(request,'blog/contact.html',{'pg':'True'})
    else:
        return render(request,'blog/contact.html')

# 搜索
def search(request):
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = "请输入关键词"
        return render(request, 'blog/index.html', {'error_msg': error_msg})
    # Q(title__icontains=q) 表示标题（title）含有关键词 q 或者正文（body）含有关键词 q
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'error_msg': error_msg,
                                               'post_list': post_list})


# from blog.models import Article
# from blog.models import Category
# from django.views.generic import ListView
# import markdown2
#
# class IndexView(ListView):
#     """
#     首页视图,继承自ListVIew，用于展示从数据库中获取的文章列表
#     """
#
#     template_name = "blog/index.html"
#     # template_name属性用于指定使用哪个模板进行渲染
#
#     context_object_name = "article_list"
#
#     # context_object_name属性用于给上下文变量取名（在模板中使用该名字）
#
#     def get_queryset(self):
#         """
#         过滤数据，获取所有已发布文章，并且将内容转成markdown形式
#         """
#         article_list = Article.objects.filter(status='p')
#         # 获取数据库中的所有已发布的文章，即filter(过滤)状态为'p'(已发布)的文章。
#         for article in article_list:
#             article.body = markdown2.markdown(article.body, )
#             # 将markdown标记的文本转为html文本
#         return article_list
#
#     def get_context_data(self, **kwargs):
#         # 增加额外的数据，这里返回一个文章分类，以字典的形式
#         kwargs['category_list'] = Category.objects.all().order_by('name')
#         return super(IndexView, self).get_context_data(**kwargs)
#
#
# class ArticleDetailView():
#     # Django有基于类的视图DetailView,用于显示一个对象的详情页，我们继承它
#     model = Article
#     # 指定视图获取哪个model
#
#     template_name = "blog/detail.html"
#     # 指定要渲染的模板文件
#
#     context_object_name = "article"
#     # 在模板中需要使用的上下文名字
#
#     pk_url_kwarg = 'article_id'
#
#     # 这里注意，pk_url_kwarg用于接收一个来自url中的主键，然后会根据这个主键进行查询
#     # 我们之前在urlpatterns已经捕获article_id
#
#     # 指定以上几个属性，已经能够返回一个DetailView视图了，为了让文章以markdown形式展现，我们重写get_object()方法。
#     def get_object(self):
#         obj = super(ArticleDetailView, self).get_object()
#         obj.body = markdown2.markdown(obj.body)
#         return obj
