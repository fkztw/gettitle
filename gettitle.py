#!/usr/bin/env python2

import argparse
import mechanize
import os
import platform
import sys

from distutils import spawn
from HTMLParser import HTMLParser


def get_args():
    p = argparse.ArgumentParser()
    p.add_argument( 'urls',
                    type   = str,
                    nargs  = '+',
                    help   = "the url(s) which you want to get its title")
    p.add_argument( '-m', '--markdown',
                    action = 'store_true',
                    help   = "output with markdown format")
    p.add_argument( '-d', '--debug',
                    action = 'store_true',
                    help   = "print debug info")

    return p.parse_args()


def set_mechanize_browser():
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [
        ('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:33.0) Gecko/20100101 Firefox/33.0'),
        ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'),
        ('Accept-Encoding', 'none'),
        ('Accept-Language', 'en-US,en;q=0.8'),
        ('Connection', 'keep-alive')
    ]

    return br

def get_real_title_and_url(br, title, url):
    # for special sites
    sites = {
        'ptt'    : "www.ptt.cc/ask/over18",
        'hackpad': "hackpad.com",
        'ruten'  : "ruten.com.tw",
    }

    if sites['ptt'] in url and any(br.forms()):
        br.form = list(br.forms())[0]
        control = br.form.find_control('yes')
        control.readonly = False
        br['yes'] = 'yes'
        br.submit()
        title = br.title()
        url   = br.geturl()

    elif sites['hackpad'] in url:
        parser = HTMLParser()
        title = parser.unescape(br.title()).encode('utf-8')

    elif sites['ruten'] in url:
        title = br.title().decode('big5').encode('utf-8')

    return title, url

def combine_title_and_url(args, title, url):
    if args.markdown:
        title = '[' + title + ']'
        url = '(' + url + ')'
        s = '{title}{url}\n'.format(title=title, url=url)
    else:
        s = '{title}\n{url}\n'.format(title=title, url=url)

    return s


def get_titles_and_urls(br, args):

    titles_and_urls = []

    for u in args.urls:

        if not any(s in u for s in ('http://', 'https://')):
            u = 'http://' + u

        try:
            r = br.open(u)
        except:
            print("unexpected error:", sys.exc_info()[0])
            exit()
        else:
            title = br.title()
            url   = br.geturl()

        if args.debug:
            # Print out webpage html for debugging
            print(r.read())
            print(title, type(title))

        title, url = get_real_title_and_url(br, title, url)
        s = combine_title_and_url(args, title, url)
        titles_and_urls.append(s)

    return titles_and_urls


def print_titles_and_urls(titles_and_urls):
    print('')
    print('\n'.join(titles_and_urls))


def copy_to_xclipboard_for_linux_users(titles_and_urls):

    text = '\n'.join(titles_and_urls)[:-1]
    # [:-1] to prevent the last '\n' to be copied.

    if platform.system() == 'Linux' and spawn.find_executable('xclip'):
        os.system(
            "echo \"{output}\" | xclip -selection clipboard".format(
                output = text
            )
        )

def main():
    args = get_args()
    br = set_mechanize_browser()
    titles_and_urls = get_titles_and_urls(br, args)
    print_titles_and_urls(titles_and_urls)
    copy_to_xclipboard_for_linux_users(titles_and_urls)


if __name__ == '__main__':
    main()
