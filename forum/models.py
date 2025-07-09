from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Modelled on walkthrough Django-Blog
STATUS = (
    (0, "Draft"),
    (1, "Published")
)


# Create your models here.
# Modelled on walkthrough Django-Blog, modified
class Article(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='articles')
    # Related_name is used to access the articles from the user
    primary_image = CloudinaryField('image', default='placeholder', blank=True, null=True)
    # New field to control how the image fits (cover, contain, etc.)
    IMAGE_FIT_CHOICES = [
        ('cover', 'Cover'),
        ('contain', 'Contain'),
        ('fill', 'Fill'),
        ('none', 'None'),
        ('scale-down', 'Scale Down'),
    ]
    primary_image_fit = models.CharField(
        max_length=20,
        choices=IMAGE_FIT_CHOICES,
        default='cover',
        help_text="How should the primary image fit inside its container?"
    )
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    updated_on = models.DateTimeField(auto_now=True)
    excerpt = models.TextField(blank=True)
    approved = models.BooleanField(default=True)

    # Order articles by date created in descending order
    class Meta:
        ordering = ['-created_on']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title).lower()
            slug = base_slug
            counter = 1
            while Article.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    # Enable more user friendly article naming
    def __str__(self):
        return f"{self.title} | created by {self.author}"


# Modelled on walkthrough Django-Blog, modified
class Comment(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)

    # Order comments by date created in descending order
    class Meta:
        ordering = ['-created_on']

    # Enable more user friendly comment naming
    def __str__(self):
        # Prevent too long a comment
        return f"Comment '{self.body[:30]}...' by {self.author} on {self.article.title}"


# New Model
class Profile(models.Model):
    USER_TYPES = (
        ('visitor', 'Visitor'),  # Default user type, not logged in
        ('member', 'Member'),  # Can comment/reply, and edit/delete own comments
        ('creator', 'Content Creator'),  # Can add articles, and edit/delete own articles
        ('moderator', 'Moderator'),  # Can approve/disapprove comments and articles
        ('admin', 'Admin'),  #  Full control(is_staff/is_superuser). Can manage users, and edit/delete any content
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='visitor')
    avatar = CloudinaryField('image', default='placeholder', blank=True, null=True)
    # Control fit of avatar
    AVATAR_FIT_CHOICES = [
        ('cover', 'Cover'),
        ('contain', 'Contain'),
        ('fill', 'Fill'),
        ('none', 'None'),
        ('scale-down', 'Scale Down'),
    ]
    avatar_fit = models.CharField(
        max_length=20,
        choices=AVATAR_FIT_CHOICES,
        default='cover',
        help_text="Control how your avatar fits in the frame."
    )
    bio = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)

    # Enable more user friendly profile naming
    def __str__(self):
        return f"{self.user.username} Profile | {self.get_user_type_display()}"
    
    # Individual permissions
    def can_view(self):
        return True  # Everyone can view

    def can_comment(self):
        return self.user_type in ['member', 'creator', 'moderator', 'admin']

    def can_reply(self):
        return self.can_comment()

    def can_edit_own_comment(self):
        return self.can_comment()

    def can_delete_own_comment(self):
        return self.can_edit_own_comment()

    def can_add_articles(self):
        return self.user_type in ['creator', 'moderator', 'admin']

    def can_edit_own_article(self):
        return self.can_add_articles()

    def can_delete_own_article(self):
        return self.can_edit_own_article()

    def can_approve_articles(self):
        return self.user_type in ['moderator', 'admin']

    def can_approve_comments(self):
        return self.user_type in ['moderator', 'admin']
    
    def can_approve_profiles(self):
        return self.user_type in ['moderator', 'admin']
    
    def can_approve_content(self):
        return (
            self.can_approve_articles()
            or self.can_approve_comments()
            or self.can_approve_profiles()
        )

    def can_manage_users(self):
        return self.is_admin()

    def is_admin(self):
        return (
            self.user_type == 'admin'
            or self.user.is_staff
            or self.user.is_superuser
        )

# Contact for collaboration and enquiry
class ContactMessage(models.Model):
    """
    Stores general enquiries and collaboration requests submitted by users.
    Accessible to admins for reading and follow-up.
    """
    email = models.EmailField()  # User's email for follow-up
    message = models.TextField()  # The message body
    created_on = models.DateTimeField(auto_now_add=True)  # Timestamp of submission
    read = models.BooleanField(default=False)  # Track whether admin has read the message

    class Meta:
        ordering = ['-created_on']  # Newest messages first

    def __str__(self):
        return f"Message from {self.email} at {self.created_on.strftime('%Y-%m-%d %H:%M')}"


# Apply for Content Creator role
class CreatorApplication(models.Model):
    """
    Represents a request by a user to become a Content Creator.
    Viewable by moderators and admins.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator_applications')  # Applicant
    reason = models.TextField()  # Justification for the role
    created_on = models.DateTimeField(auto_now_add=True)  # Timestamp of application
    approved = models.BooleanField(default=False)  # Whether the application has been approved
    reviewed = models.BooleanField(default=False)  # Whether the application has been reviewed

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"Creator application by {self.user.username}"

    def save(self, *args, **kwargs):
        # First check if approval has just been granted
        if self.approved and not self.user.profile.user_type == 'creator':
            self.user.profile.user_type = 'creator'
            self.user.profile.save()
        super().save(*args, **kwargs)


# Apply for moderator role
class ModeratorApplication(models.Model):
    """
    Represents a request by a user to become a Moderator.
    Viewable by admins only.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='moderator_applications')  # Applicant
    reason = models.TextField()  # Justification for the role
    created_on = models.DateTimeField(auto_now_add=True)  # Timestamp of application
    approved = models.BooleanField(default=False)  # Whether the application has been approved
    reviewed = models.BooleanField(default=False)  # Whether the application has been reviewed

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"Moderator application by {self.user.username}"

    def save(self, *args, **kwargs):
        if self.approved and not self.user.profile.user_type == 'moderator':
            self.user.profile.user_type = 'moderator'
            self.user.profile.save()
        super().save(*args, **kwargs)
