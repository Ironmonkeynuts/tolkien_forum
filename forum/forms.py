from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Comment, Article, Profile, ContactMessage, CreatorApplication, ModeratorApplication


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
        fields = ['user_type', 'avatar', 'bio']  # User_type to be restricted
        widgets = {
            'user_type': forms.Select(attrs={'class': 'form-select'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control-file'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        help_texts = {
            'avatar': 'Upload an avatar image for your profile (optional).',
            'bio': 'Write a short bio about yourself (optional).',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Expecting the current user to be passed in
        super().__init__(*args, **kwargs)

        if not user or not user.is_staff:
            # Hide the user_type field for non-admins
            self.fields['user_type'].disabled = True


class ApprovalToggleForm(forms.Form):
    object_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['email', 'message']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your email...'}),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe why you are contacting us. Include your name.'}),
        }
        help_texts = {
            'email': 'Include your email for our reply',
            'message': 'Describe why you are contacting us. Include your name.',
        }


class CreatorApplicationForm(forms.ModelForm):
    class Meta:
        model = CreatorApplication
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Explain why you want to become a Content Creator. Include your name.'}),
        }
        help_texts = {
            'reason': 'Explain why you want to become a Content Creator. Include your name.',
        }


class ModeratorApplicationForm(forms.ModelForm):
    class Meta:
        model = ModeratorApplication
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Explain why you want to become a Moderator. Include your name.'}),
        }
        help_texts = {
            'reason': 'Explain why you want to become a Moderator. Include your name.',
        }
