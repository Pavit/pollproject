from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('poll.views',
    url(r'^vote/(?P<poll_pk>\d)/$', 'vote', name='vote'),
    url(r'^polls/(?P<poll_pk>\d)/$', 'polls', name='polls_one'),
    url(r'^result/(?P<poll_pk>\d)/$', 'result', name='result'),
    url(r'^skip/(?P<nextpoll_pk>\d)/$', 'skip', name = 'skip'),
    url(r'^polls/', 'polls', name = 'polls'),
    url(r'^addpoll/','addpoll', name = 'addpoll'),
    (r'^thanks/', direct_to_template, {'template': 'poll/thanks.html'}),
)