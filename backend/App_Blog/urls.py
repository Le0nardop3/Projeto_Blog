from django.urls import path, include
from . import views 
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from .views import publicar, delete_post ,post_detail, editar_post

urlpatterns = [
    path('cadastro/', views.cadastro, name = 'cadastro'),
    path('login/', views.login, name = 'login'),
    path('plataforma/', views.plataforma, name = 'plataforma'),
    path('logout/', views.logout, name='logout'),
    path('publicar/', publicar, name='publicar'),
    path('meus_posts/', views.meus_posts, name = 'meus_posts'),
    path('editar_post/<int:post_id>/', editar_post, name='editar_post'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
]

