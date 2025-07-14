"""
URL configuration for tolkienforum project.

The `urlpatterns` list routes URLs to views. For more information, see:
https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import include(): from django.urls import include, path
    2. Add a URL: path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from forum import views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Rich text editor
    path('summernote/', include('django_summernote.urls')),

    # Forum routes
    path('', include('forum.urls')),
    path('forum/add/', views.article_form, name='add_article'),
    path(
        'forum/<slug:slug>/edit/',
        views.article_form,
        name='edit_article'
    ),
    path(
        'forum/<slug:slug>/delete/',
        views.ArticleDelete.as_view(),
        name='delete_article'
    ),

    # Authentication (allauth)
    path('accounts/', include('allauth.urls')),

    # Optional: built-in auth system (commented)
    # path('accounts/', include('django.contrib.auth.urls')),
]

# Custom 404 handler
handler404 = 'forum.views.custom_404'
