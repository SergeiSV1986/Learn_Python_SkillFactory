from django.urls import path
# Импортируем созданное нами представление
from .views import news_list, news_detail


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем авторам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   # path('', PostList.as_view()),
   path('news/', news_list, name='news_list'),
   path('news/<int:news_id>/', news_detail, name='news_detail'),
]