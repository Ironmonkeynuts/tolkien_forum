from django.urls import path
from . import views
from .views import ArticleList

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('forum/', ArticleList.as_view(), name='forum'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('forum/add/', views.article_form, name='add_article'),
    path('forum/<slug:slug>/', views.ArticleDetail.as_view(), name='article_detail'),
    path('forum/<slug:slug>/edit/', views.article_form, name='edit_article'),
    path('forum/<slug:slug>/delete/', views.ArticleDelete.as_view(), name='delete_article'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('toggle-approval/', views.toggle_approval, name='toggle_approval'),
]
