from django.contrib import admin
from .models import UserBookmarks, UserTags


@admin.register(UserBookmarks)
class UserBookmarksAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_bookmark_title', 'get_bookmark_url']
    list_filter = ['user']
    raw_id_fields = ['bookmark']

    @admin.display(description='书签标题')
    def get_bookmark_title(self, obj):
        return obj.bookmark.title

    @admin.display(description='URL')
    def get_bookmark_url(self, obj):
        return obj.bookmark.url


@admin.register(UserTags)
class UserTagsAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_tag_name', 'get_tag_slug']
    list_filter = ['user']

    @admin.display(description='标签名称')
    def get_tag_name(self, obj):
        return obj.tag.name

    @admin.display(description='Slug')
    def get_tag_slug(self, obj):
        return obj.tag.slug
