from django.forms import ModelForm
from Blog.models import Blog_post
from Blog.models import Post_comment
from Blog.models import Post_tag


class BlogForm(ModelForm):

    class Meta:

        model = Blog_post

        fields = (
            'titulo',
            'subtitulo',
            'contenido',
            'imagen_portada',
            'tags'
        )

    def __init__(self, *args, **kwargs):

        super(BlogForm, self).__init__(
            *args,
            **kwargs
        )

        self.fields[
            'titulo'
        ].widget.attrs.update(
            {'class': 'form-control'}
        )

        self.fields[
            'subtitulo'
        ].widget.attrs.update(
            {'class': 'form-control'}
        )

        self.fields[
            'imagen_portada'
        ].widget.attrs.update(
            {'class': 'form-control'}
        )

        self.fields[
            'tags'
        ].widget.attrs.update(
            {
                'class': 'form-select'
            }
        )


class CommentForm(ModelForm):

    class Meta:

        model = Post_comment

        fields = (
            'content',
        )

    def __init__(self, *args, **kwargs):

        super(CommentForm, self).__init__(
            *args,
            **kwargs
        )
        
class TagForm(ModelForm):

    class Meta:

        model = Post_tag

        fields = (
            'name',
            'slug'
        )