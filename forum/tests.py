from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from forum.models import Article, Comment
from forum.forms import CommentForm

User = get_user_model()


class ViewsTestCase(TestCase):
    def setUp(self):
        # Initialize Django test client
        self.client = Client()

        # Create an admin user with elevated permissions
        self.admin = User.objects.create_user(
            username='admin',
            password='adminpass'
        )
        self.admin.profile.user_type = 'admin'
        self.admin.save()

        # Create a content creator (can create articles, limited permissions)
        self.creator = User.objects.create_user(
            username='creator',
            password='creatorpass'
        )
        self.creator.profile.user_type = 'content_creator'
        self.creator.profile.save()

        # Create a standard member (cannot edit others or approve content)
        self.member = User.objects.create_user(
            username='member',
            password='memberpass'
        )
        self.member.profile.user_type = 'member'
        self.member.save()

        # Another member (used to test permission boundaries)
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass'
        )
        self.other_user.profile.user_type = 'member'
        self.other_user.profile.save()

        # Create article authored by the content creator
        self.article = Article.objects.create(
            title="Sample Article",
            slug=slugify("Sample Article"),
            content="This is a test article.",
            author=self.creator,
            status=1,
            approved=True
        )

        # Create comment ont the article by the same author
        self.comment = Comment.objects.create(
            article=self.article,
            author=self.creator,
            body="Test comment",
            approved=True
        )

    def test_article_list_view(self):
        """
        Ensure article list view is accessible and contains the article title.
        """
        response = self.client.get(reverse('forum'))
        # Page loads
        self.assertEqual(response.status_code, 200)
        # Article title present
        self.assertContains(response, "Sample Article")

    def test_article_detail_view(self):
        """
        Ensure article detail view loads and shows comment form.
        """
        response = self.client.get(
            reverse('article_detail', kwargs={'slug': self.article.slug})
        )
        # Page loads
        self.assertEqual(response.status_code, 200)
        # Content present
        self.assertContains(response, "Sample Article")
        # Form context correct
        self.assertIsInstance(response.context['form'], CommentForm)

    def test_edit_profile_own(self):
        """
        Users should be able to access their own profile edit view.
        """
        self.client.login(username='creator', password='creatorpass')
        response = self.client.get(reverse('edit_own_profile'), follow=True)
        # Page loads
        self.assertEqual(response.status_code, 200)
        # Expected content
        self.assertContains(response, "Edit Profile")

    def test_regular_user_cannot_edit_other_profile(self):
        """
        A regular user attempting to edit another user's profile
        should be redirected and shown an error message.
        """
        self.client.login(username='creator', password='creatorpass')
        # Attempt to edit someone else's profile
        url = reverse('edit_profile', kwargs={'username': 'otheruser'})
        response = self.client.get(url, follow=True)
        # Should be redirected to the profile page of that user
        expected_url = reverse('profile', kwargs={'username': 'otheruser'})
        self.assertRedirects(response, expected_url)
        # The error message should be shown on the redirected page
        self.assertContains(
            response, "You do not have permission to edit this profile."
        )
