from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('milk.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]
