from django.contrib.auth.models import User
from django.db import models


# Создание моделей.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def update_rating(self):
        # Суммарный рейтинг постов автора * 3
        post_rating = sum(post.rating * 3 for post in self.post_set.all())

        # Суммарный рейтинг комментариев, оставленных автором
        comment_ratings = sum(comment.rating for comment in self.user.comment_set.all())

        # Суммарный рейтинг комментариев к постам автора
        post_comment_rating = sum(comment.rating for post in self.post_set.all() for comment in post.comment_set.all())

        # Итоговый рейтинг
        self.rating = post_rating + comment_ratings + post_comment_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    post_type = models.CharField(max_length=10, choices=[('articles', 'Article'), ('news', 'News')], null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField()

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default='text')
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()

    def like(self):
        pass

    def dislike(self):
        pass
