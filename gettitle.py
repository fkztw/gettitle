#!/usr/bin/env python2

import sys
import mechanize

# for special sites
ptt = "www.ptt.cc/bbs"

url  = str(sys.argv[1])
br = mechanize.Browser()
br.set_handle_robots(False)
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
