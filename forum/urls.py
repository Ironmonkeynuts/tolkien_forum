from django.urls import path
from . import views
from .views import ArticleList

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('forum/', ArticleList.as_view(), name='forum'),
    path('forum/<slug:slug>/', views.ArticleDetail.as_view(), name='article_detail'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
