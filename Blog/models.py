from django.db import models
import uuid
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth.models import User
from django.urls import reverse


class Blog_post(models.Model):
    titulo = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=200, null=True, blank=True)
    contenido = CKEditor5Field(null=True, blank=True, config_name='extends')
    imagen_portada = models.ImageField(null=True, blank=True, default="default.png")
    blog_id = models.UUIDField(default= uuid.uuid4, unique=True, primary_key=True, editable=False)
    autor = models.ForeignKey(User, on_delete = models.PROTECT) 
    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Post_tag', related_name="blog_tag")

    class Meta:
        ordering = ['-date_created']
        
def __str__(self):
    return self.titulo

class Reaction_Posts(models.Model):
    Reaction_id = models.UUIDField(default= uuid.uuid4, unique=True, primary_key=True, editable=False)
    blog = models.ForeignKey(Blog_post, on_delete = models.PROTECT)
    autor = models.ForeignKey(User, on_delete = models.PROTECT)
    likes = models.ManyToManyField(User, related_name='blog_posts', verbose_name='Me Gusta')
    dislikes = models.ManyToManyField(User, related_name='blog_postss', verbose_name='No me Gusta')
    
    def total_likes(self):
        return self.likes.count()
    
    def total_dislikes(self):
        return self.dislikes.count()
      
class Post_tag (models.Model):
    name = models.CharField(max_length=255, unique=True)
    tag_id = models.UUIDField(default= uuid.uuid4, unique=True, primary_key=True, editable=False)
    slug = models.SlugField(unique=True)
    
    class Meta:
      verbose_name_plural= 'tags'  
      
    def get_absolute_url(self):
        return reverse(" Blog:tag", kwargs={"slug": self.slug })
    
    
    def __str__(self):
        return self.name
    
class Post_comment (models.Model):
    content = CKEditor5Field(null=True, blank=True, config_name='extends')
    autor = models.ForeignKey(User, on_delete = models.SET_NULL, null= True) 
    date_created = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog_post, on_delete = models.CASCADE) 
    comment_id = models.UUIDField(default= uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    
    class Meta:
        ordering = ['-date_created']
        
    def __str__(self):
        len_title = 15
        if len(self.content)> len_title:
            return self.content[len_title] +'...'
        return self.content