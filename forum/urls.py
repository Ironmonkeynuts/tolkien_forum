from django.urls import path
from . import views
from .views import ArticleList, ProfileList, Dashboard

urlpatterns = [
    path('', views.welcome, name='welcome'),

    # Forum and articles
    path('forum/', ArticleList.as_view(), name='forum'),
    path('forum/add/', views.article_form, name='add_article'),
    path(
        'forum/<slug:slug>/',
        views.ArticleDetail.as_view(),
        name='article_detail',
    ),
    path(
        'forum/<slug:slug>/edit/',
        views.article_form,
        name='edit_article',
    ),
    path(
        'forum/<slug:slug>/delete/',
        views.ArticleDelete.as_view(),
        name='delete_article',
    ),

    # Profile management
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_own_profile'),
    path(
        'profile/<str:username>/edit/',
        views.edit_profile,
        name='edit_profile',
    ),
    path(
        'profile/<str:username>/',
        views.ProfileDetail.as_view(),
        name='profile',
    ),
    path('profiles/', ProfileList.as_view(), name='profile_list'),

    # Comments
    path(
        'comment/<int:pk>/edit/',
        views.edit_comment,
        name='edit_comment',
    ),
    path(
        'comment/<int:pk>/delete/',
        views.delete_comment,
        name='delete_comment',
    ),

    # Misc
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path(
        'toggle-approval/',
        views.toggle_approval,
        name='toggle_approval',
    ),
]
