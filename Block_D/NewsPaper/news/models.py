from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username}'

    def update_rating(self):
        rate_posts = Post.objects.filter(author_id=self.id).aggregate(Sum('rating'))
        rate_comments = Comments.objects.filter(user_id=self.id).aggregate(Sum('rating'))
        rate_posts_comments = Comments.objects.filter(post__author_id=self.id).aggregate(Sum('rating'))

        self.rating = rate_posts['rating__sum'] * 3 + rate_comments['rating__sum'] + rate_posts_comments['rating__sum']
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)

    subscribers = models.ManyToManyField(User, through='CategorySubscribers')

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('category_list')


class Post(models.Model):
    news = 'N'
    article = 'A'

    POST_TYPES = [
        (news, 'Новость'),
        (article, 'Статья')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=POST_TYPES, default=news)
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)
    public = models.BooleanField(default=True)

    categorys = models.ManyToManyField(Category, through='PostCategory')

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.content[:125] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class CategorySubscribers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


