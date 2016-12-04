from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main_page, name="main_page"),
    url(r'^news/$', views.main_page_news, name="main_page_news"),
    url(r'^tops/$', views.main_page_tops, name="main_page_tops"),
    url(r'^hots/$', views.main_page_hots, name="main_page_hots"),
    url(r'^comments/(?P<pk>[0-9]+)/(?P<slug>[\w\-]+)/$', views.comments_page, name="comments_page"),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),    

    url(r'^give_point/$', views.give_point,name="give_point"),
    url(r'^make_comment/$', views.make_comment, name="make_comment"),
    url(r'^templates/(?P<template_name>[\w]+)/$',views.get_template),

]
