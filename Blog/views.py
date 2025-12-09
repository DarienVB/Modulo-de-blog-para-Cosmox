from django.shortcuts import render , redirect
from Blog.models import Blog_post, Post_tag, Reaction_Posts
from Blog.forms import BlogForm, CommentForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse

def home(request):
    blogs = Blog_post.objects.all()
    tag = Post_tag.objects.all()
    context = {'blogs':blogs, 'tag':tag}
    return render(request,'Blog/blog_page.html', context)

def blog(request, pk):
    blog= Blog_post.objects.get(id=pk)
    reaction= Reaction_Posts.objects.get(id=pk)
    total_likes = reaction.total_likes()
    total_dislikes = reaction.total_dislikes()
    context = {'blog': blog, 'reaction':reaction ,'total_likes':total_likes, 'total_dislikes':total_dislikes}
    return render(request, 'Blog/blog.html', context)

def formulario_Post(request):
    p_form = BlogForm()
    if request.method == 'POST' :
        p_form = BlogForm(request.POST, request.FILES)
        if p_form.is_valid():
            p_form.save()
            return redirect('home')
        
    context ={'p_form': p_form }
    return render (request, 'Blog/form_blog.html', context)

def formulario_Comment(request):
    c_form = CommentForm()
    if request.method == 'COMMENT' :
        c_form = CommentForm(request.COMMENT, request.FILES)
        if c_form.is_valid():
            c_form.save()
            return redirect('blog')
        
    context ={'c_form': c_form }
    return render (request, 'Blog/form_blog.html', context)

def deleteBlog(request,pk):
    blog = Blog_post.objects.get(id=pk)
    if request.method == 'POST':
        blog.delete()
        return redirect('home')
    
    context = {'blog': blog}
    return render(request, 'delete_template.html', context)

def updateBlog(request, pk):
    blog = Blog_post.objects.get(id=pk)
    form = BlogForm(instance=blog)
    update = 1
    
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance = blog)
        form.save()
        return redirect('home')
    
    context = {"form":form, "update":update}
    return render(request, 'Blog/form_blog.html', context)

def Like_View(request, pk):
    like = Reaction_Posts.objects.get(id=pk)
    dislike = Reaction_Posts.objects.get(id=pk)
    if dislike.dislikes.filter(id=request.user.id).exists():
        dislike.dislikes.remove(request.user)
        like.likes.add(request.user)
    else :
        like.likes.add(request.user)

    return HttpResponseRedirect(reverse('blog', args=[str(pk)]))

def Dislike_View(request, pk):
    like = Reaction_Posts.objects.get(id=pk)
    dislike = Reaction_Posts.objects.get(id=pk)
    if like.likes.filter(id=request.user.id).exists():
        like.likes.remove(request.user)
        dislike.dislikes.add(request.user)
    else:
        dislike.dislikes.add(request.user)

    return HttpResponseRedirect(reverse('blog', args=[str(pk)]))

def tags(request, tag_id):
    tag = Post_tag.object.get(id=tag_id)
    blogs = tag.blogs_tag.all()  
    return render(request, 'blogs/tags.html', {'tag': tag, 'blogs': blogs})
    


