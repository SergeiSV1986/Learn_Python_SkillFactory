from django.shortcuts import render
"""
# Create your views here.
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView
from .models import Author, Category, Post, PostCategory, Comment

class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'name'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'default.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'postss'
"""
from django.shortcuts import render, get_object_or_404
from .models import Post
def news_list(request):
    news = Post.objects.filter(post_type='news').order_by('-created_at')
    return render(request, 'news_list.html', {'news': news})

def news_detail(request, news_id):
    post = get_object_or_404(Post, id=news_id)
    return render(request, 'news_detail.html', {'post': post})