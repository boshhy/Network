
from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('post', views.post, name="post"),
    path('profile/<str:user>', views.profile, name="profile"),
    path('follow/<str:user>', views.follow, name="follow"),
    path('following', views.following, name='following')
]
