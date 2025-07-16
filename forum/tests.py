from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from forum.models import Article, Comment
from forum.forms import CommentForm

User = get_user_model()


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create users
        self.admin = User.objects.create_user(
            username='admin',
            password='adminpass'
        )
        self.admin.profile.user_type = 'admin'
        self.admin.save()

        self.creator = User.objects.create_user(
            username='creator',
            password='creatorpass'
        )
        self.creator.profile.user_type = 'content_creator'
        self.creator.profile.save()

        self.member = User.objects.create_user(
            username='member',
            password='memberpass'
        )
        self.member.profile.user_type = 'member'
        self.member.save()

        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass'
        )
        self.other_user.profile.user_type = 'member'
        self.other_user.profile.save()

        # Create article
        self.article = Article.objects.create(
            title="Sample Article",
            slug=slugify("Sample Article"),
            content="This is a test article.",
            author=self.creator,
            status=1,
            approved=True
        )

        # Create comment
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
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample Article")

    def test_article_detail_view(self):
        """
        Ensure article detail view loads and shows comment form.
        """
        response = self.client.get(
            reverse('article_detail', kwargs={'slug': self.article.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample Article")
        self.assertIsInstance(response.context['form'], CommentForm)

    def test_edit_profile_own(self):
        """
        Users should be able to access their own profile edit view.
        """
        self.client.login(username='creator', password='creatorpass')
        response = self.client.get(reverse('edit_own_profile'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Profile")

    def test_regular_user_cannot_edit_other_profile(self):
        """
        Regular users are redirected back to the original user's profile with an error message.
        """
        self.client.login(username='creator', password='creatorpass')

        url = reverse('edit_profile', kwargs={'username': 'otheruser'})
        response = self.client.get(url, follow=True)

        expected_url = reverse('profile', kwargs={'username': 'otheruser'})
        self.assertRedirects(response, expected_url)

        self.assertContains(response, "You do not have permission to edit this profile.")
