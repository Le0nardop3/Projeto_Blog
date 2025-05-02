from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_jg, logout as log_out
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    return redirect(login)

def cadastro(request):
    # Se o metodo for "GET" ele só renderiza o html
    if request.method == "GET":
        return render(request,'cadastro.html')
    # Se o metodo não for "GET" -> "POST"  ele faz um novo cadastro
    else:
        # fazer a coleta dos dados pelo metodo "POST"
        username = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        # Faz o teste se já tem algum usuario com esse nome antes de enviar o cadastro
        user = User.objects.filter(username=username).first()
        if user:
            message = 'Já existe um usuario com esse nome'
            return render(request, 'cadastro.html', {'message': message})
        # Caso não tenha ele cria o novo cadastro
        user = User.objects.create_user(username=username, email=email, password=senha)
        user.save()
        message2 = 'Usuario cadastrado'
        return render(request, 'cadastro.html', {'message2': message2})

def login(request):
    # Se o metodo for "GET" ele só renderiza o html
    if request.method == "GET":
        return render(request, 'login.html')
         # Se o metodo não for "GET" -> "POST"  ele faz login
    else:
        # Faz a coleta dos dados do html
        username = request.POST.get('nome')
        senha = request.POST.get('senha')
        # Coloca em uma variavel e comparar com o banco de dados
        user = authenticate(username=username, password=senha)
        # Caso esteja correto ele faz o login
        if user:
            login_jg(request, user)  
            posts = Post.objects.all()
            return redirect(plataforma)
        # Caso esteja errado ele mostra o erro
        else:
            # Caso esteja errado ele mostra o erro
            error_message = 'Nome ou senha inválidos'
            return render(request, 'login.html', {'error_message': error_message})

def plataforma(request):
    query = request.GET.get('q')
    if request.user.is_authenticated:
        if query:
            post_list = Post.objects.filter(title__icontains=query).order_by('-published_date')
        else:
            post_list = Post.objects.order_by('-published_date')

        paginator = Paginator(post_list, 8)  # Quantidade de posts por página
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # Se a página não é um número, entrega a primeira página.
            posts = paginator.page(1)
        except EmptyPage:
            # Se a página está fora dos limites, entrega a última página.
            posts = paginator.page(paginator.num_pages)

        return render(request, 'plataforma.html', {'posts': posts, 'query': query})
    return redirect('login')

def publicar(request):
    if request.method == "GET":
        form = PostForm()
        return render(request, 'publicar.html', {'form':form})
    elif request.method == "POST":
        form = PostForm(request.POST, request.FILES) 
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(plataforma)
    return render(request, 'publicar.html', {'form': form})

def meus_posts(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(author=request.user).order_by('-published_date')
        return render(request, 'meus_posts.html', {'posts': posts, 'user': request.user})
    error_message = 'Nome ou senha inválidos'
    return render(request, 'login.html', {'error_message': error_message})

def editar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'editar_post.html', {'form': form, 'post': post})

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        post.delete()
    return redirect(meus_posts)

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST, user=request.user)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect('post_detail', post_id=post_id)
    else:
        comment_form = CommentForm(user=request.user)

    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form, 'user': request.user})

def logout(request):
    log_out(request)  
    return redirect(login)

