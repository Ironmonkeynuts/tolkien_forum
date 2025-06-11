from django.db import models
from django.contrib.auth.models import User

# Modelled on walkthrough Django-Blog
STATUS = (
    (0, "Draft"),
    (1, "Published")
)


# Create your models here.
# Modelled on walkthrough Django-Blog, modified
class Article(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='articles')
    # related_name is used to access the articles from the user
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    updated_on = models.DateTimeField(auto_now=True)
    exerpt = models.TextField(blank=True)
    approved = models.BooleanField(default=False)


# Modelled on walkthrough Django-Blog, modified
class Comment(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
