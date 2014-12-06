#!/usr/bin/env python2

import sys
import mechanize

# for special sites
ptt = "www.ptt.cc/bbs"

url  = str(sys.argv[1])
br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [
    ('User-agent', "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:33.0) Gecko/20100101 Firefox/33.0"),
    ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
    ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'),
    ('Accept-Encoding', 'none'),
    ('Accept-Language', 'en-US,en;q=0.8'),
    ('Connection', 'keep-alive')
]

r = br.open(url)

if ptt in url and any(br.forms()):
    br.form = list(br.forms())[0]
    control = br.form.find_control("yes")
    control.readonly = False
    br['yes'] = 'yes'
    br.submit()

print
print br.title()
print br.geturl()
print
