from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    """
    类别
    CharField 指定了分类名 name 的数据类型，CharField 是字符型，
    CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
    其它的数据类型，日期时间类型 DateTimeField、整数类型 IntegerField 等等
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    """
    标签
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    """
    文章
    """
    # views 字段记录阅读量
    views = models.PositiveIntegerField(default=0)
    # 文章标题
    title = models.CharField(max_length=70)

    # 文章正文
    # 存储比较短的字符串可以使用 CharField，但对于文章的正文来说使用 TextField 来存储大段文本
    body = models.TextField()

    # 这两个列分别表示文章的创建时间和最后一次修改时间，存储时间的字段用 DateTimeField 类型。
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    # 文章摘要 CharField 的 blank=True 参数值后就可以允许空值了。
    excerpt = models.CharField(max_length=200, blank=True)

    # 这是分类与标签，分类与标签的模型我们已经定义在上面。
    # 我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是 ForeignKey，即一对多的关联关系。
    # 而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用 ManyToManyField，表明这是多对多的关联关系。
    # 同时我们规定文章可以没有标签，因此为标签 tags 指定了 blank=True
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 Category 类似。
    author = models.ForeignKey(User)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
    class Meta:
        ordering = ['-created_time']

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])


# Create your models here.
# class Article(models.Model):
#     """
#     类 Aticle 即表示 Blog 的文章，一个类被 diango 映射成数据库中对应的一个表，表名即类名
#     类的属性（field），比如下面的 title、body 等对应着数据库表的属性列
#     """
#     STATUS_CHOICES = (
#         ('d', 'Draft'),
#         ('p', 'Published'),
#     )
#     # 在 status 时说明
#
#     title = models.CharField('标题', max_length=70)
#     # 文章标题，CharField 表示对应数据库中表的列是用来存字符串的，'标题'是一个位置参数
#
#     body = models.TextField('正文')
#     # 文章正文，TextField 用来存储大文本字符
#
#     created_time = models.DateTimeField('创建时间', auto_now_add=True)
#     # 文章创建时间，DateTimeField用于存储时间，设定auto_now_add参数为真，则在文章被创建时会自动添加创建时间
#
#     last_modified_time = models.DateTimeField('修改时间', auto_now=True)
#     # 文章最后一次编辑时间，auto_now=True表示每次修改文章时自动添加修改的时间
#
#     status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES)
#
#     abstract = models.CharField('摘要', max_length=54, blank=True, null=True,
#                                 help_text="可选，如若为空将摘取正文的前54个字符")
#     # 文章摘要，help_text 在该 field 被渲染成 form 是显示帮助信息
#
#     views = models.PositiveIntegerField('浏览量', default=0)
#     # 阅览量，PositiveIntegerField存储非负整数
#
#     likes = models.PositiveIntegerField('点赞数', default=0)
#     # 点赞数
#
#     topped = models.BooleanField('置顶', default=False)
#     # 是否置顶，BooleanField 存储布尔值（True或者False），默认（default）为False
#
#     category = models.ForeignKey('Category', verbose_name='分类',
#                                  null=True,
#                                  on_delete=models.SET_NULL)
#
#     # 文章的分类，ForeignKey即数据库中的外键。外键的定义是：如果数据库中某个表的列的值是另外一个表的主键。外键定义了一个一对多的关系，这里即一篇文章对应一个分类，而一个分类下可能有多篇    文章。详情参考django官方文档关于ForeinKey的说明，on_delete=models.SET_NULL表示删除某个分类（category）后该分类下所有的Article的外键设为null（空）
#
#     def __str__(self):
#         # 主要用于交互解释器显示表示该类的字符串
#         return self.title
#
#     class Meta:
#         # Meta 包含一系列选项，这里的 ordering 表示排序，- 号表示逆序。即当从数据库中取出文章时，其是按文章最后一次修改时间逆序排列的。
#         ordering = ['-last_modified_time']
#
#
# class Category(models.Model):
#     """
#     另外一个表，存储文章的分类信息
#     """
#     name = models.CharField('类名', max_length=20)
#     created_time = models.DateTimeField('创建时间', auto_now_add=True)
#     last_modified_time = models.DateTimeField('修改时间', auto_now=True)
#
#     def __str__(self):
#         return self.name
