from django.apps import apps
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower
from django.core.paginator import Paginator, EmptyPage
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import (
    Article, Comment, Profile, ContactMessage,
    CreatorApplication, ModeratorApplication
)
from .forms import (
    CommentForm, ArticleForm, ProfileForm, ApprovalToggleForm, ContactForm,
    CreatorApplicationForm, ModeratorApplicationForm, UserTypeForm
)


User = get_user_model()


# Create your views here.
class ArticleList(generic.ListView):
    """
    A view that displays a list of articles with 
    search, sort, role-based filtering, and pagination.
    """
    template_name = 'forum/forum.html'
    model = Article
    context_object_name = 'object_list'
    paginate_by = 6

    def get_queryset(self):
        qs = Article.objects.all()
        search_query = self.request.GET.get('search', '')
        sort_option = self.request.GET.get('sort', '-created_on')
        user = self.request.user

        # Role-based visibility
        if user.is_authenticated:
            user_type = getattr(user.profile, 'user_type', 'visitor')

            if user.is_staff or user.is_superuser or user_type == 'admin':
                pass  # See all
            else:
                own_articles = qs.filter(author=user)
                public_articles = qs.filter(status=1, approved=True)
                qs = (own_articles | public_articles).distinct()
        else:
            qs = qs.filter(status=1, approved=True)

        # Search filtering
        if search_query:
            qs = qs.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(author__username__icontains=search_query)
            )

        # Supported sort options
        valid_sorts = [
            'title', '-title',
            'created_on', '-created_on',
            'author__username', '-author__username'
        ]

        if sort_option in valid_sorts:
            if sort_option == 'author__username':
                qs = qs.order_by(Lower('author__username'))
            elif sort_option == '-author__username':
                qs = qs.order_by(Lower('author__username').desc())
            elif sort_option == 'title':
                qs = qs.order_by(Lower('title'))
            elif sort_option == '-title':
                qs = qs.order_by(Lower('title').desc())
            else:
                qs = qs.order_by(sort_option)
        else:
            qs = qs.order_by('-created_on')  # Default

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['sort'] = self.request.GET.get('sort', '-created_on')
        return context

    # Prevent 404 on invalid page numbers
    def paginate_queryset(self, queryset, page_size):
        try:
            return super().paginate_queryset(queryset, page_size)
        except EmptyPage:
            if hasattr(self, 'paginator'):
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

    def get_queryset(self):
        """
        Ensure only published & approved articles are shown to regular users.
        Staff and superusers can view all articles (including drafts).
        """
        qs = super().get_queryset()
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return qs
        if user.is_authenticated:
            return qs.filter(
                models.Q(status=1, approved=True) |
                models.Q(author=user)
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

        if (
            self.request.user.is_authenticated
            and self.request.user == article.author
        ):
            context['comments'] = article.comments.order_by('-created_on')
        else:
            context['comments'] = article.comments.filter(
                approved=True
            ).order_by('-created_on')

        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle POST request for submitting a new comment.
        Also supports comment editing.
        """
        self.object = self.get_object()

        # Editing an existing comment
        if "edit_comment_id" in request.POST:
            comment_id = request.POST.get("edit_comment_id")
            comment = get_object_or_404(Comment, pk=comment_id)

            if (
                request.user != comment.author
                and not request.user.profile.is_admin()
            ):
                return HttpResponseForbidden(
                    "You do not have permission to edit this comment."
                )

            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                messages.success(request, "Comment updated successfully.")
                return redirect('article_detail', slug=self.object.slug)

            # If form invalid, show edit view again
            context = self.get_context_data(form=form)
            context["editing_comment_id"] = comment.id
            return self.render_to_response(context)

        # New comment submission
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = self.object
            comment.author = request.user
            comment.approved = True  # Toggle depending on moderation policy
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
                messages.success(
                    request, "Thank you! Your message has been sent.")
                return redirect('contact')
            else:
                messages.error(
                    request, "Please correct the errors in the contact form.")

        elif form_type == 'apply_creator':
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Only logged-in users can apply.")
            creator_form = CreatorApplicationForm(request.POST)
            if CreatorApplication.objects.filter(
                    user=request.user, reviewed=False).exists():
                messages.warning(
                    request,
                    "You already have a pending application."
                    )
            elif creator_form.is_valid():
                app = creator_form.save(commit=False)
                app.user = request.user  # Set user properly
                app.save()
                messages.success(
                    request,
                    ("Your application to become a "
                        "Content Creator has been submitted.")
                    )
                return redirect('contact')
            else:
                messages.error(
                    request,
                    ("Please correct the errors "
                        "in the creator application form.")
                    )

        elif form_type == 'apply_moderator':
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Only logged-in users can apply.")
            moderator_form = ModeratorApplicationForm(request.POST)
            if ModeratorApplication.objects.filter(
                    user=request.user, reviewed=False).exists():
                messages.warning(
                    request,
                    "You already have a pending application."
                    )
            elif moderator_form.is_valid():
                app = moderator_form.save(commit=False)
                # Set user properly
                app.user = request.user
                app.save()
                messages.success(
                    request,
                    ("Your application to become a Moderator "
                        "has been submitted.")
                    )
                return redirect('contact')
            else:
                messages.error(
                    request,
                    ("Please correct the errors in "
                        "the moderator application form.")
                    )

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
            request.user.profile.can_approve_content()
            or request.user.profile.is_admin()
        ):
            return HttpResponseForbidden(
                "You do not have permission to edit this article.")
    else:
        if not request.user.profile.can_add_articles():
            return HttpResponseForbidden(
                "You do not have permission to add articles.")
        article = None

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            new_article = form.save(commit=False)
            if not article:
                new_article.author = request.user
            new_article.save()
            # Smart redirect + message
            if new_article.status == 0 or not new_article.approved:
                messages.info(
                    request,
                    "Your article is saved as draft or awaiting approval."
                    )
                return redirect('forum')
            # Feedback success
            messages.success(
                request, "Your article has been saved successfully.")
            return redirect('article_detail', slug=new_article.slug)
        else:
            # Error message
            messages.error(
                request,
                ("There was an error saving your article. "
                    "Please check the form.")
                )
    else:
        form = ArticleForm(instance=article)
    return render(
        request, 
        'forum/article_form.html', {'form': form, 'article': article}
        )


@method_decorator(login_required, name='dispatch')
class ArticleDelete(generic.DeleteView):
    """
    Handles deletion of articles.
    Only the author, staff, or admin can delete.
    """
    model = Article
    success_url = '/forum/'

    def delete(self, request, *args, **kwargs):
        # Feedback on delete
        messages.success(request, "The article has been deleted.")
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
def edit_profile(request, username=None):
    """
    Handles editing of user profiles.
    Allows email updates only if Admin or User confirms their .
    Admins can also update a user's user_type.
    """
    user = request.user

    # Determine if editing own profile or another's (admin only)
    if username and (user.profile.user_type == 'admin' or user.is_staff):
        target_user = get_object_or_404(User, username=username)
    else:
        target_user = user

    editing_other = user.id != target_user.id
    profile = target_user.profile

    # Only allow editing others if admin or staff
    if editing_other and not (user.profile.user_type == 'admin'
                              or user.is_staff):
        return HttpResponseForbidden(
            "You do not have permission to edit this profile.")

    # Only allow user_type form if current user is admin
    user_type_form = (
        UserTypeForm(request.POST or None, instance=profile)
        if user.profile.user_type == 'admin' else None)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if form.is_valid():
            # First check if email is being changed
            if email and email != target_user.email:
                if user == target_user:
                    # User must confirm with own password
                    auth_user = authenticate(
                        username=user.username, password=password)
                else:
                    # Admin confirms with admin's password
                    auth_user = authenticate(
                        username=user.username, password=password)

                if auth_user:
                    target_user.email = email
                else:
                    messages.error(
                        request, "Incorrect password. Email not updated.")
                    return redirect(
                        'edit_profile',
                        username=(target_user.username
                                  if editing_other else None)
                        )

            # Now save the profile and user_type
            form.save()

            # Admin only
            if user_type_form and user_type_form.is_valid():
                user_type_form.save()

            target_user.save()

            messages.success(request, "Profile updated.")
            return redirect('profile', username=target_user.username)

        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=profile)

    # Non-admins see user_type as readonly display value
    email_initial = (target_user.email if user == target_user
                     or user.profile.user_type == 'admin' else '')
    readonly_user_type = profile.get_user_type_display()

    return render(request, 'forum/edit_profile.html', {
        'form': form,
        'user_type_form': user_type_form,
        'profile': profile,
        'editing_other': user != target_user,
        'target_user': target_user,
        'email_initial': email_initial,
        'readonly_user_type': readonly_user_type,

    })


@require_POST
def toggle_approval(request):
    """
    Handles toggling of content approval.
    """
    form = ApprovalToggleForm(request.POST)
    if form.is_valid():
        model_name = form.cleaned_data['object_type']
        object_id = form.cleaned_data['object_id']

        # Security: Ensure only known models are allowed
        if model_name not in ['Article', 'Comment', 'Profile']:
            return HttpResponseForbidden("Invalid object type.")

        model = apps.get_model('forum', model_name)
        obj = model.objects.get(pk=object_id)

        # Permissions
        if isinstance(obj, Article) and not (request.user.profile.
                                             can_approve_articles()):
            return HttpResponseForbidden("You can't approve articles.")
        elif isinstance(obj, Comment) and not (request.user.profile.
                                               can_approve_comments()):
            return HttpResponseForbidden("You can't approve comments.")
        elif isinstance(obj, Profile) and not (request.user.profile.
                                               can_approve_profiles()):
            return HttpResponseForbidden("You can't approve profiles.")

        # Toggle approval
        obj.approved = not obj.approved
        obj.reviewed = True  # Mark as reviewed on moderation
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
        return HttpResponseForbidden(
            "You do not have permission to edit this comment.")

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment updated successfully.")
            return redirect('article_detail', slug=comment.article.slug)
    else:
        form = CommentForm(instance=comment)

    return render(
        request, 'forum/edit_comment.html', {'form': form, 'comment': comment})


@login_required
def delete_comment(request, pk):
    """
    View to delete an individual comment.
    Only the author or an admin can delete.
    """
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author and not request.user.profile.is_admin():
        return HttpResponseForbidden(
            "You do not have permission to delete this comment.")

    if request.method == 'POST':
        comment.delete()
        messages.success(request, "Comment deleted.")
        return redirect('article_detail', slug=comment.article.slug)

    return render(
        request, 'forum/delete_comment_confirm.html', {'comment': comment})


class ProfileList(generic.ListView):
    """
    A view that lists approved profiles, with search and sort functionality.
    """
    model = Profile
    template_name = 'forum/profile_list.html'
    context_object_name = 'profiles'
    paginate_by = 6

    def get_queryset(self):
        """
        Returns queryset of profiles with approved articles,
        filtered by search and sorted by selected sort option.
        """
        queryset = Profile.objects.filter(approved=True)
        queryset = queryset.annotate(username_lower=Lower('user__username'))
        search = self.request.GET.get('search', '')
        sort = self.request.GET.get('sort', 'user__username')

        if search:
            queryset = queryset.filter(
                Q(user__username__icontains=search) |
                Q(bio__icontains=search)
            )

        valid_sort_options = [
            'user__username', '-user__username',
            'created_on', '-created_on'
        ]

        # Apply sort – special case for case-insensitive username
        if sort == 'user__username':
            queryset = queryset.order_by('username_lower')
        elif sort == '-user__username':
            queryset = queryset.order_by('-username_lower')
        elif sort in valid_sort_options:
            queryset = queryset.order_by(sort)
        else:
            # Default fallback
            queryset = queryset.order_by('username_lower')

        return queryset

    def get_context_data(self, **kwargs):
        """
        Add search and sort values to template context for form persistence.
        """
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
        return get_object_or_404(Profile, user__username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.filter(author=self.object.user)
        return context


# Helper function: restrict view access to moderators and admins only
def is_moderator_or_admin(user):
    return user.is_authenticated and user.profile.user_type in [
        'moderator', 'admin']


# Decorator to enforce login and user type restrictions
@method_decorator(
    [login_required, user_passes_test(is_moderator_or_admin)], name='dispatch')
class Dashboard(generic.TemplateView):
    """
    Dashboard view for moderators and admins.
    Shows tabs for:
    - Contact messages (admin only)
    - Creator applications (moderator + admin)
    - Moderator applications (admin only)
    Supports:
    - Search
    - Sort
    - Pagination
    """
    template_name = 'forum/dashboard.html'
    paginate_by = 6  # Items per page

    def get_queryset(self):
        """
        Determines the correct queryset based on active tab and user type.
        Applies optional search and sort parameters.
        """
        # Default to 'creators' tab
        tab = self.request.GET.get('tab', 'creators')
        search = self.request.GET.get('search', '').strip().lower()
        sort = self.request.GET.get('sort', '-created_on')
        user_type = self.request.user.profile.user_type

        queryset = None
        filters = Q()

        # Admins can see contact messages
        if tab == 'messages' and user_type == 'admin':
            queryset = ContactMessage.objects.all()
            if search:
                filters = (
                    Q(email__icontains=search) |
                    Q(message__icontains=search)
                )

        # Moderators and admins can view content creator applications
        elif tab == 'creators' and user_type in ['admin', 'moderator']:
            # Annotate lowercase username for case-insensitive sorting
            queryset = CreatorApplication.objects.select_related(
                'user').annotate(username_lower=Lower('user__username'))
            if search:
                filters = (
                    Q(user__username__icontains=search) |
                    Q(reason__icontains=search)
                )
                if search in ['approved', 'disapproved']:
                    filters |= Q(approved=(search == 'approved'))
                if search in ['reviewed', 'unreviewed']:
                    filters |= Q(reviewed=(search == 'reviewed'))

        # Admins can view moderator applications
        elif tab == 'moderators' and user_type == 'admin':
            # Annotate lowercase username for case-insensitive sorting
            queryset = ModeratorApplication.objects.select_related(
                'user').annotate(username_lower=Lower('user__username'))
            if search:
                filters = (
                    Q(user__username__icontains=search) |
                    Q(reason__icontains=search)
                )
                if search in ['approved', 'disapproved']:
                    filters |= Q(approved=(search == 'approved'))
                if search in ['reviewed', 'unreviewed']:
                    filters |= Q(reviewed=(search == 'reviewed'))

        # Apply search filter
        if queryset and filters:
            queryset = queryset.filter(filters)

        # Define valid sort fields including approval/review flags
        valid_sorts = {
            'messages': ['created_on', '-created_on', 'email', '-email'],
            'creators': [
                'created_on', '-created_on',
                'user__username', '-user__username',
                'approved', '-approved',
                'reviewed', '-reviewed'
            ],
            'moderators': [
                'created_on', '-created_on',
                'user__username', '-user__username',
                'approved', '-approved',
                'reviewed', '-reviewed'
            ]
        }

        # Apply sort only if valid
        if queryset:
            allowed_sorts = valid_sorts.get(tab, [])
            if sort in ['user__username', '-user__username']:
                # Use annotated lowercase username for proper sorting
                direction = '' if sort == 'user__username' else '-'
                queryset = queryset.order_by(f'{direction}username_lower')
            elif sort in allowed_sorts:
                queryset = queryset.order_by(sort)
            else:
                queryset = queryset.order_by('-created_on')  # Default fallback

        return queryset

    def get_context_data(self, **kwargs):
        """
        Adds context to the dashboard:
        - Active tab
        - Current search/sort parameters
        - Paginated results
        """
        context = super().get_context_data(**kwargs)
        tab = self.request.GET.get('tab', 'creators')
        search = self.request.GET.get('search', '')
        sort = self.request.GET.get('sort', '-created_on')
        queryset = self.get_queryset()

        # Apply pagination
        if queryset:
            paginator = Paginator(queryset, self.paginate_by)
            page_number = self.request.GET.get('page', 1)
            try:
                page_obj = paginator.get_page(page_number)
            except EmptyPage:
                page_obj = paginator.get_page(paginator.num_pages)
        else:
            page_obj = None

        context.update({
            'tab': tab,
            'search': search,
            'sort': sort,
            'page_obj': page_obj,
        })
        return context


def custom_404(request, exception=None):
    """Custom 404 error handler."""
    return render(request, '404.html', status=404)
