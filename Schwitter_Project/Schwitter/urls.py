from django.conf.urls import url
from Schwitter import views
from django.conf.urls import include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

LOGIN_URL = '/Schwitter/login/'
urlpatterns = [
    url(r'^$',views.main, name='dashboard'),
    url(r'profile/(?P<username>[\w\-]+)/$',views.viewProfile,name='view_profile'),
    url(r'login/$',views.login, name='login'),
    url(r'post/$',views.add_post,name='new_post'),
    url(r'profile/(?P<username>[\w\-]+)/(?P<title>[\w\-]+)/$',views.viewPost,name='view_post'),
    url(r'logout/$',views.user_logout,name='logout'),
    url(r'options/$',views.options,name='preferences'),
    url(r'register/$',views.register,name='register'),
    url(r'about/$',views.about,name="about"),
    ]
