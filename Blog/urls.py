from django.urls import path
from . import views



urlpatterns = [
    path('',views.home, name='home'),
    path('blog/<str:pk>', views.blog, name="blog"),#url para el contenido del blog
    path('form_blog/', views.formulario_Post, name="FormBlog"),#url para la pagina de creacion del blog
    path('form_comment/', views.formulario_Comment, name="FormComment"),
    path('delete-blog/<str:pk>/', views.deleteBlog, name="delete-blog"),#url de borrar
    path('update-blog/<str:pk>/', views.updateBlog, name="update-blog"),#url de actualizar
    path('like_blog/<str:pk>', views.Like_View, name='like_blog'),# url del like
    path('dislike_blog/<str:pk>', views.Dislike_View, name='dislike_blog'),# url del dislike
    path('tag/<int:tag_id>/', views.tags, name='tags'),
    ]
