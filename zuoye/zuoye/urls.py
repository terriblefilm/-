"""
URL configuration for zuoye project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from . import view
from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from . import test



urlpatterns = [
    path('admin/', admin.site.urls),
    path('wenda/',view.wenda, name='wenda'),
    path('login/',view.login, name='login'),
    path('signup/',view.signup, name='signup'),
    path('',view.home, name='home'),
    path('home_view/',view.home_view, name='home_view'),
    path('home_view1/',view.home_view1, name='home_view1'),
    path('chat/', view.django_view, name='chat'),
    path('signup_view/', view.signup_view, name='signup_view'),
    path('login_view/', view.login_view, name='login_view'),
    # path('home/', views.home, name='home'),
    path('password_reset/', view.PasswordResetView.as_view(), name='password_reset'),
    # 假设你有一个视图来显示服务条款
    path('terms/', view.terms_view, name='terms'),
]
