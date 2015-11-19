#!/usr/bin/env python3

import argparse
import html
import os
import platform
import traceback
import urllib
from distutils import spawn

import dryscrape
import requests
import robobrowser
from bs4 import BeautifulSoup as bs

import gettitle.exceptions
import gettitle.handles


def get_args():
    p = argparse.ArgumentParser()
    p.add_argument(
        'urls',
        metavar='url',
        type=str,
        nargs='+',
        help="url(s) of the webpage",
    )
    p.add_argument(
        '-m', '--markdown',
        action='store_true',
        help="output with markdown format",
    )
    p.add_argument(
        '-d', '--debug',
        action='store_true',
        help="print out webpage source code and title for debugging",
    )

    return p.parse_args()


def set_browser():
    br = robobrowser.RoboBrowser(parser='lxml')
    br.session.headers = {
        'User-agent': ('Mozilla/5.0 '
                       '(Macintosh; Intel Mac OS X 10.9; rv:33.0) '
                       'Gecko/20100101 Firefox/33.0'),
        'Accept': ('text/html,'
                   'application/xhtml+xml,'
                   'application/xml;'
                   'q=0.9,*/*;q=0.8'),
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }

    return br


def get_title_and_url(br, title, url, sites):

    if sites['ptt'] in url:
        form = br.get_form(action="/ask/over18")
        if form:
            br.submit_form(form, submit=form['yes'])
            page = br.parsed
            url = br.url
            title = html.unescape(page.title.string)

    return title, url


def combine_title_and_url(args, title, url):
    if args.markdown:
        title = '[' + title + ']'
        url = '(' + url + ')'
        s = '{title}{url}\n'
    else:
        s = '{title}\n{url}\n'

    return s.format(title=title, url=url)


def check_and_reconstruct_url(url):
    url = url.strip()
    url_components = urllib.parse.urlparse(url)

    if not url:
        raise gettitle.exceptions.EmptyUrlError
    elif not url_components.scheme:
        url = "{}://{}".format('http', url)
        url_components = urllib.parse.urlparse(url)
    elif url_components.scheme not in ('http', 'https'):
        url_components = url_components._replace(scheme='http')

    url = urllib.parse.urlunparse(url_components)

    return url

    if args.debug:
        traceback.print_exc()


def get_titles_and_urls(br, args):

    titles_and_urls = []
    sites = {
        'javascript': {
            'dcard': "www.dcard.tw"
        },
        'other': {
            'ptt': "www.ptt.cc/ask/over18"
        }
    }

    for url_from_user in args.urls:
        try:
            checked_url = check_and_reconstruct_url(url_from_user)
        except gettitle.exceptions.EmptyUrlError:
            continue

        for site, url in sites['javascript'].items():
            if url in checked_url:
                js_br = dryscrape.Session()
                try:
                    js_br.visit(checked_url)
                except:
                    gettitle.handles.handle_error(e, args.debug)
                else:
                    page = bs(js_br.body(), 'lxml')
                    title = html.unescape(page.title.string)
                    url = js_br.url()
                    break
        else:
            try:
                br.open(checked_url)
            except requests.exceptions.InvalidURL:
                print("InvalidURL")
            except requests.exceptions.ConnectionError as e:
                gettitle.handles.handle_error(e, args.debug, url=url_from_user)
                continue
            except:
                gettitle.handles.handle_error(e, args.debug)
            else:
                page = br.parsed
                title = html.unescape(page.title.string)
                url = br.url

        title, url = get_title_and_url(br, title, url, sites['other'])
        s = combine_title_and_url(args, title, url)
        titles_and_urls.append(s)

        if args.debug:
            print(page.prettify())
            print(title, type(title))

    return titles_and_urls


def print_titles_and_urls(titles_and_urls):
    if titles_and_urls:
        print('')
        print('\n'.join(titles_and_urls))


def copy_to_xclipboard_for_linux_users(titles_and_urls):
    text = '\n'.join(titles_and_urls)[:-1]
    # [:-1] to prevent the last '\n' to be copied.

    if platform.system() == 'Linux' and spawn.find_executable('xclip'):
        os.system(
            "echo \"{output}\" | xclip -selection clipboard".format(
                output=text
            )
        )


def main():
    args = get_args()
    br = set_browser()
    titles_and_urls = get_titles_and_urls(br, args)
    print_titles_and_urls(titles_and_urls)
    copy_to_xclipboard_for_linux_users(titles_and_urls)


if __name__ == '__main__':
    main()
