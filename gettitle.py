#!/usr/bin/env python2

import sys
import optparse
import mechanize
from HTMLParser import HTMLParser

# for special sites
ptt = 'www.ptt.cc/bbs'
hackpad = 'hackpad.com'

p = optparse.OptionParser(usage = 'usage: %prog [options] url')
p.add_option('-m', '--markdown', action = 'store_true', dest = 'markdown', help = 'output with markdown format')
p.add_option('-d', '--debug', action = 'store_true', dest = 'debug', help = 'print debug info')
opt, args = p.parse_args()


url = str(args[0])
br  = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [
    ('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:33.0) Gecko/20100101 Firefox/33.0'),
    ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
    ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'),
    ('Accept-Encoding', 'none'),
    ('Accept-Language', 'en-US,en;q=0.8'),
    ('Connection', 'keep-alive')
]

r = br.open(url)
title = br.title()
url   = br.geturl()

if opt.debug:
    print(r.read())
    print(title, type(title))

if ptt in url and any(br.forms()):
    br.form = list(br.forms())[0]
    control = br.form.find_control('yes')
    control.readonly = False
    br['yes'] = 'yes'
    br.submit()

if hackpad in url:
    parser = HTMLParser()
    title = parser.unescape(br.title()).encode('utf-8')

print('')

if (opt.markdown):
    print('[{title}]({url})'.format(title = title, url = url))
else:
    print('{title}\n{url}'.format(title = title, url = url))

print('')
