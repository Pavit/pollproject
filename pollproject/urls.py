from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
# Uncomment the next two lines to enable the admin:
from	django.contrib	import admin
#from facebook.templatetags import facebook_tags
admin.autodiscover()
import django.contrib.auth
import core
from core import views
from django.conf import settings

urlpatterns	=	patterns('',
	url(r'^admin/doc/',	include('django.contrib.admindocs.urls')),
	url(r'^poll/', include('poll.urls')),
	url(r'^admin/',	include(admin.site.urls)),
	url(r'^$', core.views.landing, name='landing'),
	url(r'^done/$', core.views.done, name='done'),
	url(r'^profile/$', core.views.profile, name = 'profile'),
	url(r'', include('social_auth.urls')),
	url(r'^logout/$', core.views.logout, name='logout'),
	(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	url(r'^admin/', include(admin.site.urls)),
	(r'^tagging_autocomplete_tagit/', include('tagging_autocomplete_tagit.urls')),
)