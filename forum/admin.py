from django.contrib import admin
from .models import Article, Comment
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Article)  # Decorator register
class ArticleAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on', 'approved')
    # Displayed fields
    search_fields = ['title', 'content']  # Searchable fields
    list_filter = ("status", "approved",)  # Filterable fields
    prepopulated_fields = {"slug": ["title",]}  # Automatically filled fields
    summernote_fields = ("content",)  # Summernote fields


# Register your models here.
admin.site.register(Comment)
