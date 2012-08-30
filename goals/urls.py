from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

from goals import views

urlpatterns = patterns('',
    url(r'^closedateset/(?P<id>\w+)/*$',        views.close_dateset,    name='close_dateset'),
    url(r'^addactivity/(?P<id>\w+)/*$',		views.add_activity, 	name='add_activity'),
    url(r'^goalset/',				views.goal_set,		name='create_goal_set'),
    url(r'^goalremove/(?P<id>\w+)/*$',          views.goal_remove,      name='remove_goal'),
    url(r'^goaladd/',				views.goal_add,         name='add_new_goal'),
    url(r'^summary/(?P<id>\w+)/*$',    		views.show_summary,     name='goals_summary'),
    url(r'^summary/*$',             		views.show_summary,     name='goals_summary'),
    url(r'^complete/*$',                        views.show_complete,    name='goalset_complete'),
    url(r'^mobile/getstarted/*$',               views.show_mobile,      name='goals_mobile'),
    url(r'^mobile/*$',                          views.show_mobile,      name='goals_mobile'),
    url(r'^$',					views.show_home,        name='goals_home'),
)

