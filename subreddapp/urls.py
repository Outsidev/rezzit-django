from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main_page, name="main_page"),
    url(r'^news/$', views.main_page_news, name="main_page_news"),
    url(r'^tops/$', views.main_page_tops, name="main_page_tops"),
    url(r'^hots/$', views.main_page_hots, name="main_page_hots"),
    url(r'^comments/(?P<pk>[0-9]+)/$', views.comments_page, name="comments_page"),

]
