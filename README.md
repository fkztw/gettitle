# Gettitle

+ A Python 3 script depends on ChromeDriver (controled by Selenium) to grab the title of webpage (even the webpages use JavaScript).
+ Support multiple urls in one command.
+ Can print out in (plaintext|markdown|rst) format.
+ Auto copy to clipboard.

---

## Requirements

+ ChromeDriver (Optional)
    + You need to install Google Chrome of course.
    + Used by Selenium in the project for some special websites.
    + You need to download the [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) and put it into some dir which is in your `$PATH`.
    + Make sure the version of Chrome is matachable with the downloaded ChromeDriver executable.
    + If you are Arch Linux user, you can install ChromeDriver via `aur/chromedriver`.
+ xclip (Optional, If you are Linux User and want to autocopy result to clipboard.)
    + Used by Pyperclip on Linux in this project.
        - No additional modules required for Windows and Mac users according to [pyperclip](https://github.com/asweigart/pyperclip).
    + For autocopy result into your clipboard, so you can just paste it to wherever you want.

---

## Installation

Requires `pip >= 19.0` (Because of using `Poetry` and `pyproject.toml`)

`$ pip install git+https://github.com/M157q/gettitle`

---

## Usage

```
usage: gettitle [-h] [-s {md,rst}] [-ul] [-c] [-d] url [url ...]

Get webpage title(s) by url(s) from terminal.

positional arguments:
  url                   url(s) of the webpage

optional arguments:
  -h, --help            show this help message and exit
  -s {md,rst}, --syntax {md,rst}
                        choose output syntax. 'md' for Markdown, 'rst' for
                        reStructuredText.
  -ul, --unordered-list
                        Enable this option for using Unordered List. Only
                        works when syntax is Markdown or reStructuredText.
  -c, --compact         output in compact mode. (No empty line between each
                        result.)
  -d, --debug           print out webpage source code and title for debugging
```

---

## Examples

### plaintext
```
$ gettitle blog.m157q.tw
================================================================================
Home | Just for noting
https://blog.m157q.tw/

================================================================================
Copied to clipboard.
```

### Markdown
```
$ gettitle -s md blog.m157q.tw
================================================================================
[Home | Just for noting](https://blog.m157q.tw/)

================================================================================
Copied to clipboard.
```

### reStructuredText
```
$ gettitle -s rst blog.m157q.tw
================================================================================
`Home | Just for noting <https://blog.m157q.tw/>`_

================================================================================
Copied to clipboard.
```

### Multiple URLs
```
$ gettitle blog.m157q.tw blog.m157q.tw
================================================================================
Home | Just for noting
https://blog.m157q.tw/

Home | Just for noting
https://blog.m157q.tw/

================================================================================
Copied to clipboard.
```

### Compact mode
```
$ gettitle -c -s md blog.m157q.tw blog.m157q.tw
================================================================================
[Home | Just for noting](https://blog.m157q.tw/)
[Home | Just for noting](https://blog.m157q.tw/)
================================================================================
Copied to clipboard.
```

---

## Testing

`$ poetry install`

`$ make test`
