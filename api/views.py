from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import BookmarkSerializer, TagSerializer
from .models import Bookmarks, Tags, BookmarkTags
from django.db.models import Q

def index(request):
    return HttpResponse("<h1>Bookmark API</h1>")

class BookmarkViewSet(viewsets.ModelViewSet):
    """
    书签 CRUD API

    列表过滤参数：
      ?favorite=1       — 只看收藏
      ?is_active=0|1    — 按可访问状态
      ?tag=<slug>       — 按标签 slug
      ?keyword=<text>   — 关键词搜索
      ?search_in=title|description|all  — 搜索范围（默认 title）
    """
    serializer_class = BookmarkSerializer
    
    def get_queryset(self):
        qs = Bookmarks.objects.order_by('-created_at')
        p = self.request.query_params

        if (favorite := p.get('favorite')) is not None:
            qs = qs.filter(is_favorite=favorite)

        if (is_active := p.get('is_active')) is not None:
            qs = qs.filter(is_active=is_active)

        if tag_slug := p.get('tag'):
            qs = qs.filter(bookmarktags__tag__slug=tag_slug)

        if keyword := p.get('keyword', '').strip():
            search_in = p.get('search_in', 'title')
            if search_in == 'description':
                qs = qs.filter(description__icontains=keyword)
            elif search_in == 'all':
                qs = qs.filter(
                    Q(title__icontains=keyword) | Q(description__icontains=keyword)
                )
            else:
                qs = qs.filter(title__icontains=keyword)

        return qs.distinct()
    
class TagViewSet(viewsets.ModelViewSet):
    """标签 CRUD API"""
    # ModelViewSet = 帮你把"操作一张数据库表"的所有标准接口（CURD）都写好了，
    # 你只需要告诉它用哪个 Model（queryset） 和用哪个 Serializer，其余按需覆盖即可。
    serializer_class = TagSerializer
    queryset = Tags.objects.all().order_by('name')