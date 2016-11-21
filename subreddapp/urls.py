from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main_page, name="main_page"),
    url(r'^comments/(?P<post_id>[0-9]+)/$', views.post_comments),
]
