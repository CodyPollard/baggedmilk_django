from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.wwdli, name='index'),
    url(r'^milkbot/$', views.milkbot, name='milkbot'),
    url(r'^timerboard/$', views.timerboard, name='timerboard'),
    url(r'pastecomparison/$', views.pastecomparison, name='pastecomparison'),
    url(r'pastecomparison/results/$', views.paste_results, name='paste-results'),
    url(r'^wwdli/$', views.wwdli, name='wwdli'),
    url(r'^wwdli/(?P<injury_id>[0-9]+)/$', views.wwdli_injury, name='wwdli-injury'),
    url(r'^wwdli-success/$', views.wwdli_success, name='wwdli-success'),
    url(r'^poll/$', views.poll, name='poll'),
]