from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^milkbot/$', views.milkbot, name='milkbot'),
    url(r'^timerboard/$', views.timerboard, name='timerboard')
]