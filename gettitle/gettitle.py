#!/usr/bin/env python3

import argparse
import sys
import urllib

import pyperclip
from selenium import webdriver

import gettitle.special_sites
import gettitle.exceptions
import gettitle.handles


def set_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:33.0) Gecko/20100101 Firefox/33.0')")
    options.add_argument("--headless")
    browser = webdriver.Chrome(options=options)
    return browser


def unset_browser(browser):
    browser.quit()


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


def visit_with_browser(browser, checked_url, debug=False):
    title, real_url = None, None

    try:
        browser.get(checked_url)
    except Exception as e:
        gettitle.handles.handle_error(e, debug)
    else:
        if debug:
            print(browser.page_source)
        title = browser.title
        real_url = browser.current_url

    for url, handler in gettitle.special_sites.URL_AND_HANDLER_MAPPING.items():
        if url in real_url:
            title, real_url = handler(browser)
            break

    return title, real_url


def get_title_and_url(browser, url, debug=False):
    try:
        checked_url = check_and_reconstruct_url(url)
    except gettitle.exceptions.EmptyUrlError:
        raise

    try:
        title, url = visit_with_browser(browser, checked_url, debug)
    except Exception as e:
        gettitle.handles.handle_error(e)

    return title.strip(), url.strip()


def get_titles_and_urls(browser, args):
    titles_and_urls = []

    for url_from_user in args.urls:
        try:
            title, url = get_title_and_url(browser, url_from_user, args.debug)
        except Exception:
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
    try:
        pyperclip.copy(text)
    except Exception as e:
        gettitle.handles.handle_error(e, debug)
    else:
        print("Copied result to clipboard.")


def main():
    args = get_args()

    try:
        browser = set_browser()
    except Exception as e:
        gettitle.handles.handle_error(e)
    else:
        titles_and_urls = get_titles_and_urls(browser, args)
    finally:
        unset_browser(browser)

    print_titles_and_urls(titles_and_urls)
    copy_result_to_clipboard_for_users(titles_and_urls, args.debug)


if __name__ == '__main__':
    status = main()
    sys.exit(status)
