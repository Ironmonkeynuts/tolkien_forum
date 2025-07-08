"""
URL configuration for tolkienforum project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from forum import views
from django.shortcuts import render


def trigger_404(request):
    """
    A view function that raises a 404 error.
    This function is used for testing purposes.
    """
    return render(request, '404.html', status=404)


urlpatterns = [
    path('admin/', admin.site.urls),  # URL for the Django admin site
    path('summernote/', include('django_summernote.urls')),
    # URL for the Summernote editor
    path('', include('forum.urls')),
    # URL for the forum view
    path('forum/add/', views.article_form, name='add_article'),
    # URL for adding an article
    path('forum/<slug:slug>/edit/', views.article_form, name='edit_article'),
    # URL for editing an article
    path('forum/<slug:slug>/delete/', views.ArticleDelete.as_view(), name='delete_article'),
    # URL for deleting an article
    path('accounts/', include('allauth.urls')),
    # URL for allauth authentication
    path('accounts/', include('django.contrib.auth.urls')),
    # URL for built-in Django authentication
    path('test-404/', trigger_404),

]

handler404 = 'forum.views.custom_404'
