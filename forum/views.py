from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage
from django.contrib import messages
from .models import Article, Comment, Profile, ContactMessage, CreatorApplication, ModeratorApplication
from .forms import CommentForm, ArticleForm, ProfileForm, ApprovalToggleForm, ContactForm, CreatorApplicationForm, ModeratorApplicationForm


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
    # Prevent 404 if users request invalid page
    def paginate_queryset(self, queryset, page_size):
        try:
            return super().paginate_queryset(queryset, page_size)
        except EmptyPage:
            if hasattr(self, 'paginator'):  # Ensure paginator exists
                return self.paginator.page(self.paginator.num_pages)
            return super().paginate_queryset(queryset, page_size)


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
        if self.request.user.is_authenticated:
            return qs.filter(
                models.Q(status=1, approved=True) |
                models.Q(author=self.request.user)
            )
        return qs.filter(status=1, approved=True)

    def get_context_data(self, **kwargs):
        """
        Add additional context:
        - Approved comments for this article
        - A blank comment form for users to submit new comments
        """
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        # Allow author to see their own unapproved comments
        if self.request.user.is_authenticated and self.request.user == article.author:
            context['comments'] = article.comments.order_by('-created_on')
        else:
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
        # Check if this is an edit request
        if "edit_comment_id" in request.POST:
            comment_id = request.POST.get("edit_comment_id")
            comment = get_object_or_404(Comment, pk=comment_id)

            if request.user != comment.author and not request.user.profile.is_admin():
                return HttpResponseForbidden("You do not have permission to edit this comment.")

            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                messages.success(request, "Comment updated successfully.")
                return redirect('article_detail', slug=self.object.slug)

            # If form invalid, keep context and editing state
            context = self.get_context_data(form=form)
            context["editing_comment_id"] = comment.id
            return self.render_to_response(context)

        # Handle new comment submission
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = self.object
            comment.author = request.user
            comment.approved = True  # or False, depending on moderation
            comment.save()
            messages.success(request, 'Your comment has been posted.')
            return redirect('article_detail', slug=self.object.slug)

        context = self.get_context_data(form=form)
        return self.render_to_response(context)


def welcome(request):
    return render(request, 'forum/welcome.html')


def profile(request):
    return render(request, 'forum/profile.html')


def about(request):
    return render(request, 'forum/about.html')


@csrf_protect
def contact(request):
    contact_form = ContactForm()
    creator_form = CreatorApplicationForm()
    moderator_form = ModeratorApplicationForm()

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'contact':
            contact_form = ContactForm(request.POST)
            if contact_form.is_valid():
                contact_form.save()
                messages.success(request, "Thank you! Your message has been sent.")
                return redirect('contact')
            else:
                messages.error(request, "Please correct the errors in the contact form.")

        elif form_type == 'apply_creator':
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Only logged-in users can apply.")
            creator_form = CreatorApplicationForm(request.POST)
            if CreatorApplication.objects.filter(user=request.user, reviewed=False).exists():
                messages.warning(request, "You already have a pending application.")
            elif creator_form.is_valid():
                app = creator_form.save(commit=False)
                app.user = request.user  # Set user properly
                app.save()
                messages.success(request, "Your application to become a Content Creator has been submitted.")
                return redirect('contact')
            else:
                messages.error(request, "Please correct the errors in the creator application form.")

        elif form_type == 'apply_moderator':
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Only logged-in users can apply.")
            moderator_form = ModeratorApplicationForm(request.POST)
            if ModeratorApplication.objects.filter(user=request.user, reviewed=False).exists():
                messages.warning(request, "You already have a pending application.")
            elif moderator_form.is_valid():
                app = moderator_form.save(commit=False)
                app.user = request.user  # Set user properly
                app.save()
                messages.success(request, "Your application to become a Moderator has been submitted.")
                return redirect('contact')
            else:
                messages.error(request, "Please correct the errors in the moderator application form.")

    context = {
        'contact_form': contact_form,
        'creator_form': creator_form,
        'moderator_form': moderator_form,
    }
    return render(request, 'forum/contact.html', context)


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
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            new_article = form.save(commit=False)
            if not article:
                new_article.author = request.user
            new_article.save()
            if new_article.status == 0 or not new_article.approved:  # Smart redirect + message
                messages.info(request, "Your article is saved as draft or awaiting approval.")
                return redirect('forum')
            messages.success(request, "Your article has been saved successfully.")  # Feedback success
            return redirect('article_detail', slug=new_article.slug)
        else:
            messages.error(request, "There was an error saving your article. Please check the form.")  # Error message
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

    def delete(self, request, *args, **kwargs):
        messages.success(request, "The article has been deleted.")  # Feedback on delete
        return super().delete(request, *args, **kwargs)

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

@login_required
def edit_profile(request):
    """
    Handles editing of user profiles.
    """
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")  # Feedback success
            return redirect('profile')
        else:
            messages.error(request, "There was an error updating your profile. Please check the form.")  # Error message
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'forum/edit_profile.html', {'form': form})


def toggle_approval(request):
    """
    Handles toggling of content approval.
    """
    form = ApprovalToggleForm(request.POST)
    if form.is_valid():
        model_name = form.cleaned_data['object_type']
        object_id = form.cleaned_data['object_id']
        model = apps.get_model('forum', model_name)

        obj = model.objects.get(pk=object_id)

        # Permissions
        if isinstance(obj, Article) and not request.user.profile.can_approve_articles():
            return HttpResponseForbidden("You can't approve articles.")
        elif isinstance(obj, Comment) and not request.user.profile.can_approve_comments():
            return HttpResponseForbidden("You can't approve comments.")
        elif isinstance(obj, Profile) and not request.user.profile.can_approve_profiles():
            return HttpResponseForbidden("You can't approve profiles.")

        # Toggle approval
        obj.approved = not obj.approved
        obj.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def edit_comment(request, pk):
    """
    View to edit an individual comment.
    Only the author or an admin can edit.
    """
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author and not request.user.profile.is_admin():
        return HttpResponseForbidden("You do not have permission to edit this comment.")

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment updated successfully.")
            return redirect('article_detail', slug=comment.article.slug)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'forum/edit_comment.html', {'form': form, 'comment': comment})


@login_required
def delete_comment(request, pk):
    """
    View to delete an individual comment.
    Only the author or an admin can delete.
    """
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author and not request.user.profile.is_admin():
        return HttpResponseForbidden("You do not have permission to delete this comment.")

    if request.method == 'POST':
        comment.delete()
        messages.success(request, "Comment deleted.")
        return redirect('article_detail', slug=comment.article.slug)

    return render(request, 'forum/delete_comment_confirm.html', {'comment': comment})


class ProfileList(generic.ListView):
    """
    View to list all user profiles.
    """
    model = Profile
    template_name = 'forum/profile_list.html'
    context_object_name = 'profiles'
    paginate_by = 12

    def get_queryset(self):
        """
        Returns queryset of profiles with approved articles.
        """
        queryset = Profile.objects.filter(approved=True)
        search = self.request.GET.get('search', '')
        sort = self.request.GET.get('sort', 'user__username')

        if search:
            queryset = queryset.filter(
                Q(user__username__icontains=search) |
                Q(bio__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['sort'] = self.request.GET.get('sort', 'user__username')
        return context


class ProfileDetail(generic.DetailView):
    """
    View to display details of a user profile.
    """
    model = Profile
    template_name = 'forum/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        username = self.kwargs.get('username')
        return Profile.objects.select_related('user').get(user__username=username)
