# Gettitle  
  
+ A Python 3 script depends on ChromeDriver (controled by Selenium) to grab the title of webpage (even the webpages use JavaScript).  
+ Support multiple urls in one command.  
+ Can print out in (plaintext|markdown|rst) format.  
+ Auto copy to clipboard.  
  
---  
  
## Requirements  
  
+ [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)  
  
---  
  
## Installation  
  
`$ pip install git+https://github.com/M157q/gettitle`  
  
---  
  
## Usage  
  
```  
usage: gettitle [-h] [-s {md,rst}] [-c] [-d] url [url ...]  
  
positional arguments:  
  url                   url(s) of the webpage  
  
optional arguments:  
  -h, --help            show this help message and exit  
  -s {md,rst}, --syntax {md,rst}  
                        choose output syntax. 'md' for Markdown, 'rst' for  
                        reStructuredText.  
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
  
`$ python -m unittest`  
