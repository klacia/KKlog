from django.conf.urls.defaults import *
import os.path

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(os.path.dirname(__file__), 'static'),}),
    (r'^admin/', include(admin.site.urls)),
    (r'', include('KKlog.blog.urls')),
)
