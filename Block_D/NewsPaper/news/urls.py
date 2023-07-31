from django.urls import path
from .views import PostList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('news/', PostList.as_view(), name='post_list'),
    path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('news/search/', PostSearch.as_view(), name='post_search'),
    path('news/create/', PostCreate.as_view(), name='post_create_news'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='post_edit_news'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete_news'),
    path('articles/create/', PostCreate.as_view(), name='post_create_articles'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='post_edit_articles'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='post_delete_articles'),
]
