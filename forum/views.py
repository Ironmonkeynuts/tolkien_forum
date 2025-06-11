from django.shortcuts import render
from django.views import generic
from .models import Article


# Create your views here.
class ArticleList(generic.ListView):
    """
    A view that displays a list of articles.
    """
    queryset = Article.objects.filter(status=1)
    template_name = 'article_list.html'
