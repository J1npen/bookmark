from rest_framework import serializers
from .models import Bookmarks, Tags, BookmarkTags
from django.utils import timezone

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['id','name','slug','color']

class BookmarkSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tags.objects.all(),
        write_only=True,
        required=False,
        help_text='要关联的标签 ID 列表，传入后会替换原有全部标签',
    )
    
    class Meta:
        model = Bookmarks
        fields = [
            'id', 'title', 'url', 'description', 'favicon_url',
            'is_domestic', 'site_scale', 'is_active', 'is_favorite',
            'visit_count', 'last_visit', 'created_at', 'updated_at',
            'tags', 'tag_ids',
        ]
        read_only_fields = ['visit_count', 'last_visit', 'created_at', 'updated_at']

    def get_tags(self, obj):
        qs = Tags.objects.filter(bookmarktags__bookmark=obj)
        return TagSerializer(qs, many=True).data
    
    def create(self, validated_data):
        tag_objs = validated_data.pop('tag_ids', [])
        now = timezone.now()
        validated_data.setdefault('visit_count', 0)
        validated_data.setdefault('created_at', now)
        validated_data.setdefault('updated_at', now)
        bookmark = Bookmarks.objects.create(**validated_data)
        if tag_objs:
            BookmarkTags.objects.bulk_create([
                BookmarkTags(bookmark=bookmark, tag=tag) for tag in tag_objs
            ])
        return bookmark
    
    def update(self, instance, validated_data):
        tag_objs = validated_data.pop('tag_ids')
        now = timezone.now()
        validated_data['update_at'] = now
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tag_objs is not None:
            BookmarkTags.objects.filter(bookmark=instance).delete()
            if tag_objs:
                BookmarkTags.objects.bulk_create([
                    BookmarkTags(bookmark=instance, tag=tag) for tag in tag_objs
                ])
        return instance