from django.conf import settings
from django.db import models
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Autor')
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=200, verbose_name='titulo')
    text = models.TextField()  
    created_date = models.DateTimeField(default=timezone.now, verbose_name='Criado em')
    published_date = models.DateTimeField(blank=True, null=True, verbose_name='Publicado em')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.text