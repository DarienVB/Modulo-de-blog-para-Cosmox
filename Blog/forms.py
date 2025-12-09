from django.forms import ModelForm
from django import forms
from Blog.models import Blog_post, Post_comment

class BlogForm(ModelForm):
    class Meta:
        model = Blog_post
        fields ="titulo", "subtitulo", "contenido","imagen_portada", "autor"
    
    def __init__ (self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
    
    
        self.fields['titulo'].widget.attrs.update({'class': 'form-control'})
        self.fields['subtitulo'].widget.attrs.update({'class': 'form-control'})
        self.fields['imagen_portada'].widget.attrs.update({'class': 'form-control'})
        
class CommentForm(ModelForm):
    class Meta:
        model = Post_comment
        fields ="content", "autor"
    
    def __init__ (self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)

    
    