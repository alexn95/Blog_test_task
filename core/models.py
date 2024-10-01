from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.db import models

from core.magers import PostManager


class User(AbstractBaseUser):
    login = models.CharField(max_length=100, unique=True, verbose_name='Login')
    email = models.EmailField(unique=True, verbose_name='Email')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')

    USERNAME_FIELD = 'login'
    objects = UserManager()

    def __str__(self):
        return self.login

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Comment(models.Model):
    content = models.TextField(verbose_name='Content')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, verbose_name='Post', related_name='comments')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Title')
    content = models.TextField(verbose_name='Content')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='Published at')
    likes = models.PositiveIntegerField(default=0, verbose_name='Likes')
    tags = models.ManyToManyField(Tag, verbose_name='Tags', related_name='posts', blank=True)

    objects = PostManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
