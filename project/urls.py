from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^__debug__/', include(debug_toolbar.urls)),
    url(r'', include('quiz.urls')),
]
