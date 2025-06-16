from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Article, Comment, Profile


@admin.register(Article)  # Decorator register
class ArticleAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on', 'approved')
    # Displayed fields
    search_fields = ['title', 'content', 'author__username']  # Searchable fields
    list_filter = ("status", "created_on", "approved",)  # Filterable fields
    prepopulated_fields = {"slug": ("title",)}  # Automatically filled fields
    summernote_fields = ("content",)  # Summernote fields


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
    # Displayed fields
    search_fields = ('user__username', 'user_type')  # Searchable fields
    list_filter = ('user_type', 'approved')  # Filterable fields
