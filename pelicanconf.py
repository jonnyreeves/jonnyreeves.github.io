#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Jonny Reeves'
SITENAME = u'Jonny Reeves'
SITEURL = ''
SITETITLE = 'Jonny Reeves'
SITESUBTITLE = 'code && coffee || music'
TIMEZONE = 'Europe/London'
DEFAULT_LANG = u'en'
MAIN_MENU = False

ARTICLE_URL = '{date:%Y}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{slug}/index.html'
ARTICLE_EXCLUDES = ['extra']

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.toc': {},
    },
    'output_format': 'html5',
}

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

DISQUS_SITENAME = 'jonnyreeves'

GOOGLE_ANALYTICS = 'UA-30309890-1'

# Social widget
SOCIAL = (('linkedin', 'https://br.linkedin.com/in/jonnyreeves/en'),
          ('github', 'https://github.com/jonnyreeves'),)

# Blogroll
LINKS = (
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

STATIC_PATHS = ['images', 'extra/CNAME', 'extra/google184ba0b4352bb6cd.html']
EXTRA_PATH_METADATA = { 'extra/CNAME': {'path': 'CNAME'},
                        'extra/google184ba0b4352bb6cd.html': {'path': 'google184ba0b4352bb6cd.html'},
}

# Flex Theme Settings
THEME="./pelican-themes/Flex"
SITELOGO='/images/avatar.jpg'
FAVICON='/images/favicon.ico'

OPENSOURCE = (
	('jonnyreeves/js-logger', 'Lightweight, unobtrusive, configurable JavaScript logger.'),
	('jonnyreeves/fetch-readablestream', 'Compatibility layer for efficient streaming of binary data using WHATWG Streams'),
	('improbable-eng/ts-protoc-gen', 'Protocol Buffers Compiler (protoc) plugin for TypeScript and gRPC-Web.'),
	('jonnyreeves/as3-vanilla', 'Extract strongly typed Objects from dynamic objects without writing a single line of code!'),
	('jonnyreeves/jquery-Mustache', ' Mustache templating plugin for jQuery.'),
)

# SVBHack Theme Settings
#THEME="../pelican-themes/Flex"
#USER_LOGO_URL=SITEURL + '/images/avatar.jpg'
