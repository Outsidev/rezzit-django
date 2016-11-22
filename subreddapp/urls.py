from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main_page, name="main_page"),
    url(r'^comments/(?P<pk>[0-9]+)/$', views.post_comments, name="post_comments"),
]
