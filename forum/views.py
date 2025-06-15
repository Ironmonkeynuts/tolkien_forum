from django.shortcuts import render
from django.views import generic
from .models import Article


# Create your views here.
class ArticleList(generic.ListView):
    """
    A view that displays a list of articles.
    """
    queryset = Article.objects.filter(status=1, approved=True)
    template_name = 'forum/forum.html'
    paginate_by = 3


def welcome(request):
    return render(request, 'forum/welcome.html')

def profile(request):
    return render(request, 'forum/profile.html')

def about(request):
    return render(request, 'forum/about.html')

def contact(request):
    return render(request, 'forum/contact.html')