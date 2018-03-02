"""s6day145_luffy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from api.yrykj_urls import views as api
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', api.LoginView.as_view()),
    url(r'^courses/$', api.CoursesView.as_view()),
    url(r'^news/$', api.NewsView.as_view()),
    url(r'^courses/(?P<pk>\d+)\.(?P<format>[a-z0-9]+)$', api.CoursesView.as_view()),
    url(r'^news/(?P<pk>\d+)\.(?P<format>[a-z0-9]+)$', api.NewsView.as_view()),
    url(r'^comment/$', api.CommentView.as_view()),
    url(r'^agree/$', api.AgreeView.as_view()),
    url(r'^collect/$', api.CollectView.as_view()),
    url(r'^shopping_car/$', api.ShoppingCarView.as_view()),
    url(r'^course/buy/$', api.Course_buy.as_view()),
]
