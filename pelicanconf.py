#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Jonny Reeves'
SITENAME = u'Jonny Reeves'
SITEURL = ''
TIMEZONE = 'Europe/London'
DEFAULT_LANG = u'en'

ARTICLE_URL = '{date:%Y}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{slug}/index.html'


# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

GOOGLE_ANALYTICS = 'UA-30309890-1'

# Blogroll
LINKS = (
	('Github', 'http://github.com/jonnyreeves'),
	('Stack Overflow', 'http://stackoverflow.com/users/227349/jonnyreeves'),
	('+JonnyReeves', 'https://plus.google.com/+JohnReeves')
)

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

STATIC_PATHS = ['images', 'extra/CNAME']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},}

# SVBHack Theme Settings
THEME="../pelican-themes/pelican-svbhack"
USER_LOGO_URL=SITEURL + '/images/avatar.jpg'
