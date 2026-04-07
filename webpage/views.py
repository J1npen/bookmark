from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from api.models import Bookmarks, Tags, BookmarkTags
from django.core.paginator import Paginator
from django.utils import timezone

@login_required
def index(request):
    filter_keyword = request.GET.get('keyword', '').strip()
    tag_slug      = request.GET.get('tag', '').strip()
    search_in     = request.GET.get('search_in', 'title')  # title | description | all

    queryset = Bookmarks.objects.prefetch_related(
        'bookmarktags_set__tag'
    ).order_by('-id')

    if filter_keyword:
        if search_in == 'description':
            queryset = queryset.filter(description__icontains=filter_keyword)
        elif search_in == 'all':
            queryset = queryset.filter(
                Q(title__icontains=filter_keyword) |
                Q(description__icontains=filter_keyword)
            )
        else:  # title (默认)
            queryset = queryset.filter(title__icontains=filter_keyword)

    if tag_slug:
        queryset = queryset.filter(bookmarktags__tag__slug=tag_slug)

    try:
        per_page = int(request.GET.get('per_page', 21))
        per_page = max(3, min(per_page, 60))
    except (ValueError, TypeError):
        per_page = 21

    paginator  = Paginator(queryset, per_page)
    page_obj   = paginator.get_page(request.GET.get('page', 1))
    all_tags   = Tags.objects.all().order_by('name')

    return render(request, 'webpage/index.html', {
        'page_obj' : page_obj,
        'keyword'  : filter_keyword,
        'tag_slug' : tag_slug,
        'search_in': search_in,
        'all_tags' : all_tags,
        'per_page' : str(per_page),
    })

@login_required
def bookmark_visit(request, pk):
    """记录点击次数并跳转"""
    bookmark = get_object_or_404(Bookmarks, pk=pk)
    Bookmarks.objects.filter(pk=pk).update(
        visit_count=bookmark.visit_count + 1,
        last_visit=timezone.now()
    )
    return redirect(bookmark.url)