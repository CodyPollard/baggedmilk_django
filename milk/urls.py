from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^milkbot/$', views.milkbot, name='milkbot'),
    url(r'^timerboard/$', views.timerboard, name='timerboard'),
    url(r'pastecomparison/$', views.pastecomparison, name='pastecomparison'),
    url(r'pastecomparison/results/$', views.paste_results, name='paste-results'),
    url(r'^wwdli/$', views.wwdli, name='milkbot'),

]