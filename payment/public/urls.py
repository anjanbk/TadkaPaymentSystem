from django.conf.urls.defaults import patterns, include, url

from public import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^signup/$', views.signup, name='signup'),
	url(r'^help/$', views.songhelp, name='help'),
	#url(r'^/signup/$', views.signup, name='signup'),
)
