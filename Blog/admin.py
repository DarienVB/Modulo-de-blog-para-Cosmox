from django.contrib import admin
from .models import Blog_post, Post_tag, Post_comment, Reaction_Posts
# Register your models here.
admin.site.register(Blog_post)
admin.site.register(Post_comment)
admin.site.register(Post_tag)
admin.site.register(Reaction_Posts)


