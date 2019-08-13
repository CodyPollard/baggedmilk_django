from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^milkbot/$', views.milkbot, name='milkbot'),
    url(r'^timerboard/$', views.timerboard, name='timerboard'),
    url(r'pastecomparison/$', views.pastecomparison, name='pastecomparison'),
    url(r'pastecomparison/results/$', views.paste_results, name='paste-results'),
    # WWDLI
    url(r'^wwdli/$', views.wwdli, name='wwdli'),
    url(r'^wwdli/(?P<injury_id>[0-9]+)/$', views.wwdli_injury, name='wwdli-injury'),
    url(r'^wwdli-success/$', views.wwdli_success, name='wwdli-success'),
    url(r'^wwdli/roster/ducks$', views.wwdli_roster_ducks, name='wwdli_roster_ducks'),
    # Misc
    url(r'^poll/$', views.poll, name='poll'),
    url(r'^download/eljefe-jeffe', views.jeff_xml, name='jeff-xml'),
]