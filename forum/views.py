from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Article, Comment
from .forms import CommentForm


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
    Also handles comment display and submission.
    """
    model = Article
    template_name = 'forum/article_detail.html'
    context_object_name = 'article'
    form_class = CommentForm

    # Filter out drafts/unapproved articles for non-staff users
    def get_queryset(self):
        """
        Ensure only published & approved articles are shown to regular users.
        Staff and superusers can view all articles (including drafts/unapproved).
        """
        qs = super().get_queryset()
        if self.request.user.is_staff or self.request.user.is_superuser:
            return qs
        return qs.filter(status=1, approved=True)

    def get_context_data(self, **kwargs):
        """
        Add additional context:
        - Approved comments for this article
        - A blank comment form for users to submit new comments
        """
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        # Fetch approved comments only, order newest first
        context['comments'] = article.comments.filter(approved=True).order_by('-created_on')
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle POST request for submitting a new comment.
        - Validate form
        - Link comment to article & user
        - Save (with approval required unless auto-approve is enabled)
        - Redirect to the article detail page to avoid form resubmission
        """
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = self.object
            comment.author = request.user
            comment.approved = True  # Automatic approval
            comment.save()
            # Redirect to the same page so a refresh doesn't resubmit the form
            return redirect('article_detail', slug=self.object.slug)
        else:
            # If form is invalid, re-render with errors and existing context
            context = self.get_context_data(form=form)
            return self.render_to_response(context)

def welcome(request):
    return render(request, 'forum/welcome.html')


def profile(request):
    return render(request, 'forum/profile.html')


def about(request):
    return render(request, 'forum/about.html')


def contact(request):
    return render(request, 'forum/contact.html')
