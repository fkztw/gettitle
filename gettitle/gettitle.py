#!/usr/bin/env python3

import argparse
import html
import platform
import subprocess
import sys
import urllib
from distutils import spawn

import dryscrape
import requests
import robobrowser
from bs4 import BeautifulSoup as bs

import gettitle.constants
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
    session = requests.Session()
    session.verify = False
    no_js_br = robobrowser.RoboBrowser(parser='lxml', session=session)
    no_js_br.session.headers = {
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

    try:
        dryscrape.start_xvfb()
    except:
        pass

    try:
        js_br = dryscrape.Session()
    except:
        js_br = None

    return {'no_js': no_js_br, 'js': js_br}


def combine_title_and_url(args, title, url):
    title = title.strip().replace('\n', ' ')
    url = url.strip()

    if args.markdown:
        title = '[' + title.replace('[', r'\[').replace(']', r'\]') + ']'
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

    return urllib.parse.urlunparse(url_components)


def visit_with_js_browser(js_br, url, debug=False):
    page, title, real_url = None, None, None

    try:
        js_br.visit(url)
    except:
        gettitle.handles.handle_error(sys.exc_info()[0], debug)
    else:
        page = bs(js_br.body(), 'lxml')
        title = html.unescape(page.title.string)
        real_url = js_br.url()

        if debug:
            print(page.prettify())

    if page is None:
        raise RuntimeError('page is None')

    return title, real_url


def visit_with_no_js_browser(br, url, debug=False):
    page, title, real_url = None, None, None

    try:
        br.open(url)
    except requests.exceptions.InvalidURL:
        print("Invalid URL")
    except requests.exceptions.ConnectionError as e:
        print(e)
        gettitle.handles.handle_error(e, debug, url=url)
        raise gettitle.exceptions.ConnectionError
    except Exception as e:
        gettitle.handles.handle_error(e, debug)
    else:
        page = br.parsed
        real_url = br.url
        try:
            title = html.unescape(page.title.string)
        except:
            raise

    if gettitle.constants.sites['ptt'] in real_url:
        form = br.get_form(action="/ask/over18")
        if form:
            br.submit_form(form, submit=form['yes'])
            page = br.parsed
            real_url = br.url
            title = html.unescape(page.title.string)

    if page is None:
        raise RuntimeError('page is None')

    if debug:
        print(page.prettify())

    return title, real_url


def get_title_and_url(br, url, debug=False):
    try:
        checked_url = check_and_reconstruct_url(url)
    except gettitle.exceptions.EmptyUrlError:
        raise

    try:
        title, url = visit_with_no_js_browser(br['no_js'], checked_url, debug)
    except gettitle.exceptions.ConnectionError:
        raise
    except:
        try:
            title, url = visit_with_js_browser(br['js'], checked_url, debug)
        except:
            raise

    return title.strip(), url.strip()


def get_titles_and_urls(br, args):
    titles_and_urls = []

    for url_from_user in args.urls:
        try:
            title, url = get_title_and_url(br, url_from_user, args.debug)
        except:
            continue
        else:
            s = combine_title_and_url(args, title, url)
            titles_and_urls.append(s)

        if args.debug:
            print(title, type(title))

    return titles_and_urls


def print_titles_and_urls(titles_and_urls):
    if titles_and_urls:
        print('')
        print('\n'.join(titles_and_urls))


def copy_result_to_clipboard_for_users(titles_and_urls, debug=False):
    '''
    This function currently only support Linxu users with `xclip` installed.
    '''
    # [:-1] to prevent the last '\n' to be copied.
    text = '\n'.join(titles_and_urls)[:-1]

    escape_text_for_shell = text.replace(r'"', r'\"')

    user_os = platform.system()
    if debug:
        print("user_os: {}".format(user_os))
    if user_os != 'Linux':
        # currently support using xclip on Linux only.
        return

    xclip_path = spawn.find_executable('xclip') or ''
    if debug:
        print("xclip_path: {}".format(xclip_path))
    if not xclip_path:
        return

    xclip_copy_command = (
        'echo -e "{}" | {} -selection clipboard &> /dev/null'
    ).format(
        escape_text_for_shell,
        xclip_path,
    )
    if debug:
        print("xclip_copy_command: {}".format(xclip_copy_command))

    try:
        completed_process = subprocess.run(xclip_copy_command, shell=True, check=True)
    except:
        print("Something wrong with xclip. The content won't be copied.")
    else:
        print("Copied result to clipboard via xclip.")
        if debug:
            print(completed_process)


def main():
    args = get_args()
    br = set_browser()
    titles_and_urls = get_titles_and_urls(br, args)
    print_titles_and_urls(titles_and_urls)
    copy_result_to_clipboard_for_users(titles_and_urls, args.debug)


if __name__ == '__main__':
    status = main()
    sys.exit(status)
