from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Comment, Article, Profile


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Your comment...'}),
        }


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'excerpt', 'primary_image', 'content', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'primary_image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'content': SummernoteWidget(),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        help_texts = {
            'primary_image': 'Upload a primary image for the article (optional).',
            'content': 'Write your article content here.',
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_type', 'avatar', 'bio']
        widgets = {
            'user_type': forms.Select(attrs={'class': 'form-select'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control-file'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        help_texts = {
            'avatar': 'Upload an avatar image for your profile (optional).',
            'bio': 'Write a short bio about yourself (optional).',
        }
