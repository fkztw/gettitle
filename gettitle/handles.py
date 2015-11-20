import traceback

import requests


def handle_error(e, debug, url=None):
    def handle_unexpected_error():
        if not debug:
            traceback.print_exc()

        print('')
        print('='*20)
        print("Unexpected Error Happened.")
        bug_report_url = "https://github.com/M157q/gettitle/issues"
        t = "Please report the error message above to {}"
        print(t.format(bug_report_url))
        print('='*20)
        exit()

    def handle_connection_error(url):
        t = 'Check your network connection or the URL "{}" is invalid.'
        print(t.format(url))

    if debug:
        traceback.print_exc()

    if isinstance(e, requests.exceptions.ConnectionError):
        if url:
            handle_connection_error(url)
    else:
        handle_unexpected_error()
