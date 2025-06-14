from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Article, Comment


@admin.register(Article)  # Decorator register
class ArticleAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on', 'approved')
    # Displayed fields
    search_fields = ['title', 'content']  # Searchable fields
    list_filter = ("status", "created_on", "approved",)  # Filterable fields
    prepopulated_fields = {"slug": ("title",)}  # Automatically filled fields
    summernote_fields = ("content",)  # Summernote fields


# Register your models here.
# admin.site.register(Article)
admin.site.register(Comment)
