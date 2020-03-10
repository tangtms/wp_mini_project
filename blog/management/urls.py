from django.urls import path
from . import views

urlpatterns = [
    path('post/add/', views.post_add, name='post_add'),
    path('post/edit/<int:post_id>/', views.post_update, name='post_update'),
    path('post/all/', views.post_list, name='post_list'),
    path('post/<int:post_id>/', views.detail, name='post_detail'),
    path('post/comment_delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),
    path('post/comment_edit/<int:comment_id>/', views.comment_edit, name='comment_edit'),
    path('post/hide/<int:post_id>/', views.post_hide, name='post_hide'),
    path('post/show/<int:post_id>/', views.post_show, name='post_show')
    
]