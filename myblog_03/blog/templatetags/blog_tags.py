#!usr/bin/env python  
# -*- coding:utf-8 -*-
from django import template
from django.db.models.aggregates import Count
from ..models import Post, Category,Tag

register = template.Library()
# 最新文章排序
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]
# 时间归档统计
@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')
# 文章分类数量统计
@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
# 文章的标签分类
@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)