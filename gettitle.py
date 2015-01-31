#!/usr/bin/env python2

import sys
import argparse
import mechanize
from HTMLParser import HTMLParser

def main():
    # for special sites
    sites = {
        'ptt'    : "www.ptt.cc/ask/over18",
        'hackpad': "hackpad.com",
        'ruten'  : "goods.ruten.com.tw",
    }

    p = argparse.ArgumentParser()
    p.add_argument( 'url',
                    type   = str,
                    help   = "the url which you want to get its title")
    p.add_argument( '-m', '--markdown',
                    action = 'store_true',
                    help   = "output with markdown format")
    p.add_argument( '-d', '--debug',
                    action = 'store_true',
                    help   = "print debug info")
    args = p.parse_args()

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

    r = br.open(args.url)
    title = br.title()
    url   = br.geturl()

    if args.debug:
        print(r.read())
        print(title, type(title))

    if sites['ptt'] in url and any(br.forms()):
        br.form = list(br.forms())[0]
        control = br.form.find_control('yes')
        control.readonly = False
        br['yes'] = 'yes'
        br.submit()
        title = br.title()
        url   = br.geturl()

    if sites['hackpad'] in url:
        parser = HTMLParser()
        title = parser.unescape(br.title()).encode('utf-8')

    if sites['ruten'] in url:
        title = br.title().decode('big5').encode('utf-8')

    print('')

    if (args.markdown):
        print('[{title}]({url})'.format(title = title, url = url))
    else:
        print('{title}\n{url}'.format(title = title, url = url))

    print('')


if __name__ == '__main__':
    main()
