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

    # Order articles by date created in descending order
    class Meta:
        ordering = ['-created_on']

    # Enable more user friendly article naming
    def __str__(self):
        return f"{self.title} | Created by {self.author}"


# Modelled on walkthrough Django-Blog, modified
class Comment(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    # Order comments by date created in descending order
    class Meta:
        ordering = ['-created_on']

    # Enable more user friendly comment naming
    def __str__(self):
        return f"Comment {self.body} by {self.author} on {self.article.title}"
