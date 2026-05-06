from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter

app_name = "api"

router = DefaultRouter()
router.register('bookmarks', views.BookmarkViewSet, basename='api-bookmark')
router.register('tags', views.TagViewSet, basename='api-tag')

urlpatterns = [
    path('', views.index, name='index'),
    path('describe/', views.describe_url, name='describe-url'),
    path('', include(router.urls)),
]