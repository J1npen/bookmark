from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from .serializers import BookmarkSerializer, TagSerializer
from .models import Bookmarks, Tags, BookmarkTags, UserBookmarks, UserTags
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
        user = self.request.user
        if user.is_superuser:
            qs = Bookmarks.objects.order_by('-created_at')
        else:
            qs = Bookmarks.objects.filter(
                userbookmarks__user=user
            ).order_by('-created_at')

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

    def perform_create(self, serializer):
        bookmark = serializer.save()
        UserBookmarks.objects.create(user=self.request.user, bookmark=bookmark)

    def destroy(self, request, *args, **kwargs):
        bookmark = self.get_object()
        UserBookmarks.objects.filter(user=request.user, bookmark=bookmark).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TagViewSet(viewsets.ModelViewSet):
    """标签 CRUD API"""
    serializer_class = TagSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Tags.objects.all().order_by('name')
        return Tags.objects.filter(usertags__user=user).order_by('name')

    def perform_create(self, serializer):
        tag = serializer.save()
        UserTags.objects.create(user=self.request.user, tag=tag)

    def destroy(self, request, *args, **kwargs):
        tag = self.get_object()
        UserTags.objects.filter(user=request.user, tag=tag).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)