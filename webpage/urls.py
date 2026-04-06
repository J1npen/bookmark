from django.urls import path, include
from . import views

app_name = "webpage"

urlpatterns = [
    path('', views.index, name='bookmark'),
    path('<int:pk>/visit/', views.bookmark_visit, name='bookmark_visit'),
]