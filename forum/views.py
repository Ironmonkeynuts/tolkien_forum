from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.db import models
from .models import Article, Comment
from .forms import CommentForm, ArticleForm


# Create your views here.
class ArticleList(generic.ListView):
    """
    A view that displays a list of articles.
    """

    template_name = 'forum/forum.html'
    paginate_by = 6

    def get_queryset(self):
        qs = Article.objects.all()

        if self.request.user.is_authenticated:
            # Staff see all
            if self.request.user.is_staff or self.request.user.is_superuser: 
                return qs
            else:
                # Authors see their own drafts and/or unapproved articles
                own_articles = qs.filter(author=self.request.user)
                public_articles = qs.filter(status=1, approved=True)
                return (own_articles | public_articles).distinct()
        else:
            # Public users see only approved published articles
            return qs.filter(status=1, approved=True)
        except EmptyPage:


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
        # Let creators see their own drafts and pending
        return qs.filter(
            models.Q(status=1, approved=True) |
            models.Q(author=self.request.user)
        )

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


@login_required
def article_form(request, slug=None):
    """
    Handles both article creation and editing:
    - If slug provided → edit mode.
    - If no slug → create mode.
    Permissions:
    - Create: content creator, moderator, admin.
    - Edit: author, moderator, admin.
    """
    if slug:
        article = get_object_or_404(Article, slug=slug)
        if request.user != article.author and not (
            request.user.profile.can_approve_content() or request.user.profile.is_admin()
        ):
            return HttpResponseForbidden("You do not have permission to edit this article.")
    else:
        if not request.user.profile.can_add_articles():
            return HttpResponseForbidden("You do not have permission to add articles.")
        article = None

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            new_article = form.save(commit=False)
            if not article:
                new_article.author = request.user
            new_article.save()
            return redirect('article_detail', slug=new_article.slug)
        else:
            # return form with errors
            return render(
                request,
                'forum/article_form.html',
                {'form': form, 'article': article}
            )
    else:
        form = ArticleForm(instance=article)

    return render(request, 'forum/article_form.html', {'form': form, 'article': article})


@method_decorator(login_required, name='dispatch')
class ArticleDelete(generic.DeleteView):
    """
    Handles deletion of articles.
    Only the author, staff, or admin can delete.
    """
    model = Article
    success_url = '/forum/'

    def get_queryset(self):
        """
        Restricts deletion rights to:
        - The author
        - Staff/admins
        """
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs
        return qs.filter(author=self.request.user)