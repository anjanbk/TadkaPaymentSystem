from django.conf.urls.defaults import patterns, include, url

import os.path

PWD = os.path.dirname(os.path.realpath(__file__ )) 

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'payment.views.home', name='home'),
    # url(r'^payment/', include('payment.foo.urls')),
    #url(r'^$', views.index, name='index'),
    url(r'^public/', include('public.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': os.path.join(PWD,'../media/')}),
)
