from django.urls import path
from . import views



urlpatterns = [
    path('',views.home, name='home'),
    path('logout/',views.logoutUser,name='logout'),
    path('blog/<str:pk>', views.blog, name="blog"),
    path('form_blog/', views.formulario_Post, name="FormBlog"),
    path('form_comment/<str:pk>/',views.formulario_Comment,name="FormComment"),
    path('delete-blog/<str:pk>/', views.deleteBlog, name="delete-blog"),
    path('update-blog/<str:pk>/', views.updateBlog, name="update-blog"),
    path('like_blog/<str:pk>', views.Like_View, name='like_blog'),
    path('dislike_blog/<str:pk>', views.Dislike_View, name='dislike_blog'),
    path('update-comment/<str:pk>/',views.updateComment,name='update-comment'),
    path('delete-comment/<str:pk>/',views.deleteComment,name='delete-comment'),
    path('tags-admin/',views.administrarTags,name='tags-admin'),
    path('create-tag/',views.createTag,name='create-tag'),
    path('delete-tag/<str:pk>/',views.deleteTag,name='delete-tag'),
    path('login/',views.loginUser,name='login'),
    ]

