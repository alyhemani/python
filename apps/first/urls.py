from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^main$', views.main),
    url(r'^logout$', views.logout),
    url(r'^add$', views.add),
    url(r'^users/(?P<id>\d+)$', views.users),
    url(r'^favorite/(?P<id>\d+)$', views.favorite),
    url(r'^remove/(?P<id>\d+)$', views.remove),
]
