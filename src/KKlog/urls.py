from django.conf.urls.defaults import patterns, include
from django.contrib import admin
import os.path

admin.autodiscover()

urlpatterns = patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(os.path.dirname(__file__), 'static'),}),
    (r'^admin/', include(admin.site.urls)),
    (r'', include('KKlog.blog.urls')),
)
