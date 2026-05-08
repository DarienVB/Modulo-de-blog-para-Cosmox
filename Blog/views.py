from django.shortcuts import render , redirect
from Blog.models import Blog_post, Post_tag, Reaction_Posts, Post_comment
from Blog.forms import BlogForm, CommentForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from Blog.forms import TagForm
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.core.paginator import Paginator

def home(request):

    query = request.GET.get(
        'q',
        ''
    )

    order = request.GET.get(
        'order',
        'desc'
    )


    blogs = Blog_post.objects.all()


    if query:

        blogs = blogs.filter(

            Q(
                titulo__icontains=query
            )

            |

            Q(
                tags__name__icontains=query
            )

        ).distinct()


    if order == 'asc':

        blogs = blogs.order_by(
            'date_created'
        )

    else:

        blogs = blogs.order_by(
            '-date_created'
        )


    paginator = Paginator(
        blogs,
        5
    )


    page_number = request.GET.get(
        'page'
    )


    page_obj = paginator.get_page(
        page_number
    )


    context = {

        'blogs': page_obj,

        'query': query,

        'order': order

    }


    return render(

        request,

        'Blog/blog_page.html',

        context

    )

def blog(request, pk):

    blog = Blog_post.objects.get(
        blog_id=pk
    )

    reaction, created = Reaction_Posts.objects.get_or_create(
    blog=blog
    )

    comments = Post_comment.objects.filter(
        blog=blog
    )

    context = {
        'blog': blog,
        'reaction': reaction,
        'comments': comments,
        'total_likes': reaction.total_likes(),
        'total_dislikes': reaction.total_dislikes()
    }

    return render(
        request,
        'Blog/blog.html',
        context
    )
    
@login_required   
def formulario_Post(request):

    p_form = BlogForm()

    if request.method == 'POST':

        p_form = BlogForm(
            request.POST,
            request.FILES
        )

        if p_form.is_valid():

            blog = p_form.save(
                commit=False
            )

            blog.autor = request.user

            blog.save()

            p_form.save_m2m()

            Reaction_Posts.objects.get_or_create(
                blog=blog
            )

            messages.success(
              request,
              'Blog creado correctamente'
            )
            return redirect(
               'home'
            )
        else:  messages.error(
               request,
               'Ocurrió un error'
            )
    context = {
        'p_form': p_form
    }

    return render(
        request,
        'Blog/form_blog.html',
        context
    )
    
@login_required    
def formulario_Comment(
    request,
    pk
):

    blog = Blog_post.objects.get(
        blog_id=pk
    )

    c_form = CommentForm()

    if request.method == 'POST':

        c_form = CommentForm(
            request.POST
        )

        if c_form.is_valid():

            comment = c_form.save(
                commit=False
            )

            comment.autor = request.user

            comment.blog = blog

            comment.save()
            messages.success(
              request,
              'Comentario creado correctamente'
            ) 
            return redirect(
                'blog',
                pk
            )
        else: messages.error(
               request,
               'Ocurrió un error'
            )
           

    context = {
        'c_form': c_form
    }

    return render(
        request,
        'Blog/form_comment.html',
        context
    )
    
@login_required
def deleteBlog(request, pk):

    blog = Blog_post.objects.get(
        blog_id=pk
    )

    if (
        blog.autor != request.user
        and
        not request.user.is_superuser
    ):

        return HttpResponseForbidden()
    if request.method == 'POST':
        blog.delete()
        messages.success(
            request,
            'Blog eliminado correctamente'
        )
        return redirect('home')
    context = {'blog': blog}
    return render(request, 'Blog/delete_blog.html', context)

@login_required
def updateBlog(request, pk):

    blog = Blog_post.objects.get(
        blog_id=pk
    )

    if (
        blog.autor != request.user
        and
        not request.user.is_superuser
    ):

        return HttpResponseForbidden()

    form = BlogForm(
        instance=blog
    )

    update = True

    if request.method == 'POST':

        form = BlogForm(
            request.POST,
            request.FILES,
            instance=blog
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Blog actualizado correctamente'
            )

            return redirect(
                'home'
            )

        else:

            messages.error(
                request,
                'Ocurrió un error'
            )

    context = {
        'p_form': form,
        'update': update
    }

    return render(
        request,
        'Blog/form_blog.html',
        context
    )

@login_required
def Like_View(request, pk):

    reaction = Reaction_Posts.objects.get(
        blog__blog_id=pk
    )

    if reaction.dislikes.filter(
        id=request.user.id
    ).exists():

        reaction.dislikes.remove(
            request.user
        )

    reaction.likes.add(
        request.user
    )

    return HttpResponseRedirect(
        reverse(
            'blog',
            args=[str(pk)]
        )
    )

@login_required
def Dislike_View(request, pk):

    reaction = Reaction_Posts.objects.get(
        blog__blog_id=pk
    )

    if reaction.likes.filter(
        id=request.user.id
    ).exists():

        reaction.likes.remove(
            request.user
        )

    reaction.dislikes.add(
        request.user
    )

    return HttpResponseRedirect(
        reverse(
            'blog',
            args=[str(pk)]
        )
    )
    
@login_required
def tags(request, tag_id):
    tag = Post_tag.objects.get(tag_id=tag_id)
    blogs = tag.blog_tag.all()  
    return render(request, 'blogs/tags.html', {'tag': tag, 'blogs': blogs})
    
@login_required
def updateComment(request, pk):

    comment = Post_comment.objects.get(
        comment_id=pk
    )
    if (
        comment.autor != request.user
        and
        not request.user.is_superuser
    ):

        return HttpResponseForbidden()
    
    form = CommentForm(
        instance=comment
    )

    if request.method == 'POST':

        form = CommentForm(
            request.POST,
            instance=comment
        )

        if form.is_valid():

            form.save()
            messages.success(
              request,
              'Comentario actualizado correctamente'
            )
            return redirect(
                'blog',
                comment.blog.blog_id
            )
        else:  messages.error(
               request,
               'Ocurrió un error'
            )
            

    context = {
        'c_form': form
    }

    return render(
        request,
        'Blog/form_comment.html',
        context
    )

@login_required
def deleteComment(request, pk):

    comment = Post_comment.objects.get(
        comment_id=pk
    )

    if (
        comment.autor != request.user
        and
        not request.user.is_superuser
    ):

        return HttpResponseForbidden()

    blog_pk = comment.blog.blog_id

    if request.method == 'POST':

        comment.delete()
        messages.success(
            request,
            'Comentario eliminado correctamente'
        )
        return redirect(
            'blog',
            blog_pk
        )
    context = {
        'comment': comment
    }

    return render(
        request,
        'Blog/delete_comment.html',
        context
    )
    
@login_required
def administrarTags(request):

    if request.user.is_superuser:

        tags = Post_tag.objects.all()

    else:

        tags = Post_tag.objects.filter(
            autor=request.user
        )

    context = {
        'tags': tags
    }

    return render(
        request,
        'Blog/tags_admin.html',
        context
    )

@login_required
def createTag(request):

    form = TagForm()

    if request.method == 'POST':

        form = TagForm(
            request.POST
        )

        if form.is_valid():

            tag = form.save(
                commit=False
            )

            tag.autor = request.user

            tag.save()
            messages.success(
              request,
              'Categoria creado correctamente'
            )
            return redirect(
                'tags-admin'
            )
        else: messages.error(
               request,
               'Ocurrió un error'
            )

            

    context = {
        'form': form
    }

    return render(
        request,
        'Blog/form_tag.html',
        context
    )    
    
@login_required
def deleteTag(request, pk):

    tag = Post_tag.objects.get(
        tag_id=pk
    )

    if (
    tag.autor != request.user
    and
    not request.user.is_superuser
     ):
        return HttpResponseForbidden()

    if request.method == 'POST':

        tag.delete()
        messages.success(
            request,
            'Categoria eliminada correctamente'
        )
        return redirect(
            'tags-admin'
        )
    context = {
        'tag': tag
    }

    return render(
        request,
        'Blog/delete_tag.html',
        context
    )
    
def loginUser(request):

    if request.user.is_authenticated:

        return redirect(
            'home'
        )

    if request.method == 'POST':

        username = request.POST.get(
            'username'
        )

        password = request.POST.get(
            'password'
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(
                request,
                user
            )

            messages.success(
                request,
                'Sesión iniciada'
            )

            return redirect(
                'home'
            )

        else:

            messages.error(
                request,
                'Usuario o contraseña incorrectos'
            )

    return render(
        request,
        'Blog/login.html'
    )
    
@login_required
def logoutUser(request):

    logout(
        request
    )

    messages.success(
        request,
        'Sesión cerrada'
    )

    return redirect(
        'home'
    )        
