import os
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BookmarkSerializer, TagSerializer
from .models import Bookmarks, Tags, BookmarkTags, UserBookmarks, UserTags
from django.db.models import Q

def index(request):
    return HttpResponse("<h1>Bookmark API</h1>")


@api_view(['GET'])
def describe_url(request):
    url = request.query_params.get('url', '').strip()
    if not url:
        return Response({'description': ''})
    try:
        import httpx
        from bs4 import BeautifulSoup
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import SystemMessage, HumanMessage
        import re

        with httpx.Client(timeout=10, follow_redirects=True) as client:
            resp = client.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            html = resp.text

        soup = BeautifulSoup(html, 'html.parser')

        # 提取 title
        title_tag = soup.find('title')
        page_title = title_tag.get_text(strip=True) if title_tag else ''

        # 提取 meta description（og:description 优先级更高）
        meta = (soup.find('meta', attrs={'property': 'og:description'}) or
                soup.find('meta', attrs={'name': 'description'}))
        meta_desc = meta.get('content', '').strip() if meta else ''

        # 提取正文
        body_text = soup.get_text(' ', strip=True)[:2000]

        # 组装上下文
        context_parts = []
        if page_title:
            context_parts.append(f'网站标题：{page_title}')
        if meta_desc:
            context_parts.append(f'网站描述（meta）：{meta_desc}')
        if body_text:
            context_parts.append(f'页面正文：{body_text}')
        context = '\n'.join(context_parts).strip()[:2000]

        # 内容质量检测：过滤掉纯空白、过短的无效内容
        meaningful_text = re.sub(r'\s+', '', context)
        if len(meaningful_text) < 30:
            return Response({'description': '', 'reason': 'content_too_short'})

        llm = ChatOpenAI(
            model='gpt-4o-mini',
            api_key=os.environ.get('OPENAI_API_KEY', ''),
            base_url=os.environ.get('OPENAI_BASE_URL', 'https://api.openai.com'),
            temperature=0.3,
        )

        system_prompt = (
            '你是一个网页内容摘要助手。'
            '请严格根据用户提供的网页信息生成描述，禁止凭借领域知识推断或补充页面未提及的内容。'
            '若页面内容含义不明或严重不足，请只输出：页面内容不足，建议手动填写描述。\n\n'
            '格式要求：\n'
            '- 输出 1-2 句中文，直接输出描述，不加任何前缀\n'
            '- 中英文混排时，在中文字符与英文、数字、符号之间加一个半角空格（如"使用 Python 构建"而非"使用Python构建"）'
        )
        user_prompt = (
            f'请根据以下网页信息，总结这个网页的主要内容和用途：\n\n'
            f'URL：{url}\n'
            f'{context}'
        )

        result = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ])

        description = result.content.strip()

        # 后处理兜底：用正则补全 AI 遗漏的中英文间空格
        # 在中文字符之后、英文/数字之前补空格
        description = re.sub(r'([\u4e00-\u9fff\u3000-\u303f])([A-Za-z0-9])', r'\1 \2', description)
        # 在英文/数字之后、中文字符之前补空格
        description = re.sub(r'([A-Za-z0-9])([\u4e00-\u9fff\u3000-\u303f])', r'\1 \2', description)

        return Response({'description': description})
    except Exception:
        return Response({'description': ''})

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