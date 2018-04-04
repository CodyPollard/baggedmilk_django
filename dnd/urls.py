from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dice/$', views.dice, name='dice'),
    url(r'^shops/$', views.shops, name='shops'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]