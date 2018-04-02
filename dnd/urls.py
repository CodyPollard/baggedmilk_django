from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dice/$', views.dice, name='dice'),
    url(r'^shops/$', views.shops, name='shops'),
]