django-goaltracking
===================

	django-goaltracking is an app built to work with the Django framework, modelled after many famous goal setting/personal success programs.  The idea is to start with a large list of goals, anything you can imagine you might want to do with your life, then whittle those down to just four that you want to focus on over the course of a twelve-week program.  During those twelve weeks (they're five-day weeks, the weekends are free) you keep a record of the steps you've taken each day that move you forward with each of the four goals you've chosen.  I run it locally, to keep track of my own progress on a set of chosen goals, but I'm in the process of getting it live that other people can use it without having to install code.

Requirements:

	Python 2.7
	Django 1.3
	A database (my local version runs with Postgres)

Getting Started:

	Install Django 1.3 if you don't already have it - the documentation can be found here: https://docs.djangoproject.com/en/1.3/topics/install/

	Check this project out to a local folder and adjust your settings.  Aside from the standard settings for Django 1.3, you'll need to be sure you define:

	STATICFILES_DIRS (I'm using "~/django-goaltracking/static")

	TEMPLATE_DIRS (I'm using "~/django-goaltracking/templates/" as well as my local path to the Django admin templates)

	Add the goals app to INSTALLED_APPS:

	INSTALLED_APPS = (
		...
		'django-goaltracking.goals',
		...
	)

Usage Notes:

	The models are simple, based on the notion that smaller, interconnected relations are better.  Each user owns a list of goals.  When four goals are chosen for a twelve-week program, those four goals are collected in a goalset.  For every day of the twelve-week program there is a dateset (the date, plus one instance of each of the four goals) and activities (related to a specific goal on a specific date).

	There are a few extraneous models: quotes (for inspirational quotes that appear to the user each day) and static content (descriptive copy that does not vary from user to user, e.g., 'about' copy, descriptions of the user flow, etc.) that can be plugged into any page, anywhere via a call to a templatetag.

Still To Do:

	I'm working on a mobile version, which will most likely leverage jQuery Mobile.  That should be up by August 31.

	I also haven't added tests yet, so use at your own risk until then.

Contact Information:

	See the app in action: http://www.4-goals.com (coming soon)
	Twitter: @bshaurette
        My developer site: http://www.mechanicalgirl.com

Last Revised:

	August 23, 2012

