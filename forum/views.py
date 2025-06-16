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
    paginate_by = 6

class ArticleDetail(generic.DetailView):
    """
    A view that displays the details of a specific article.
    """
    model = Article
    template_name = 'forum/article_detail.html'
    context_object_name = 'article'

    # Filter out drafts/unapproved articles for non-staff users
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_staff or self.request.user.is_superuser:
            return qs
        return qs.filter(status=1, approved=True)


def welcome(request):
    return render(request, 'forum/welcome.html')


def profile(request):
    return render(request, 'forum/profile.html')


def about(request):
    return render(request, 'forum/about.html')


def contact(request):
    return render(request, 'forum/contact.html')
