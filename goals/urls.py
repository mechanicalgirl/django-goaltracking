from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

from goals import views

urlpatterns = patterns('',
    url(r'^closedateset/(?P<id>\w+)/*$',        views.close_dateset,    name='close_dateset'),
    url(r'^addactivity/(?P<id>\w+)/*$',		views.add_activity, 	name='add_activity'),
    url(r'^goalset/',				views.goal_set,		name='create_goal_set'),
    url(r'^goaladd/',				views.goal_add,         name='add_new_goal'),
    url(r'^summary/(?P<id>\w+)/*$',             views.show_summary,     name='goals_summary'),
    url(r'^summary/*$',             		views.show_summary,     name='goals_summary'),
    url(r'^about/$', 				direct_to_template, 	{'template': 'about.html'}),
    url(r'^$',					views.show_home,        name='goals_home'),
)

