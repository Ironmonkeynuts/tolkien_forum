from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import (
    Article, Comment, Profile,
    ContactMessage, CreatorApplication, ModeratorApplication
)


@admin.register(Article)  # Decorator register
class ArticleAdmin(SummernoteModelAdmin):
    # Displayed fields
    list_display = ('title', 'slug', 'status', 'created_on', 'approved')
    # Searchable fields
    search_fields = ['title', 'content', 'author__username']
    # Filterable fields
    list_filter = ("status", "created_on", "approved",)
    # Automatically filled fields
    prepopulated_fields = {"slug": ("title",)}
    # Summernote fields
    summernote_fields = ("content",)


# Register your models here.
# admin.site.register(Article)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('body', 'article', 'author', 'created_on', 'approved')
    # Displayed fields
    search_fields = ('body', 'author__username')  # Searchable fields
    list_filter = ('created_on', 'approved')  # Filterable fields

    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
    approve_comments.short_description = "Approve selected comments"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'approved')
    search_fields = ('user__username', 'user_type')
    list_filter = ('user_type', 'approved')

    # Make user_type editable in the form
    fields = ('user', 'user_type', 'avatar', 'bio', 'approved')

    # Restrict editing to prevent changes to already approved users
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.approved:
            return ['user_type']  # Prevent editing user_type after approval
        return []    # Displayed fields
    search_fields = ('user__username', 'user_type')  # Searchable fields
    list_filter = ('user_type', 'approved')  # Filterable fields


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_on')
    search_fields = ('email', 'message')


@admin.register(CreatorApplication)
class CreatorApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_on', 'approved', 'reviewed')
    search_fields = ('user__username', 'reason')
    list_filter = ('approved', 'reviewed')
    actions = ['approve_selected']

    def approve_selected(self, request, queryset):
        queryset.update(approved=True)
    approve_selected.short_description = "Approve selected applications"


@admin.register(ModeratorApplication)
class ModeratorApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_on', 'approved', 'reviewed')
    search_fields = ('user__username', 'reason')
    list_filter = ('approved', 'reviewed')
    actions = ['approve_selected']

    def approve_selected(self, request, queryset):
        queryset.update(approved=True)
    approve_selected.short_description = "Approve selected applications"
