# Gettitle  
  
A Python 3 script depends on ChromeDriver (controled by Selenium) to grab the title of webpage (even the webpages use JavaScript).  
Can print out in normal or markdown format.  
Currently support auto copy to clipboard via `xclip`.  
  
---  
  
## Requirements  
  
+ [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)  
  
---  
  
## Installation  
  
`$ pip install git+https://github.com/M157q/gettitle`  
  
---  
  
## Usage  
  
```  
usage: gettitle [-h] [-s {md,rst}] [-d] url [url ...]  
  
positional arguments:  
  url                   url(s) of the webpage  
  
optional arguments:  
  -h, --help            show this help message and exit  
  -s {md,rst}, --syntax {md,rst}  
                        choose output syntax. 'md' for Markdown, 'rst' for  
                        reStructuredText.  
  -d, --debug           print out webpage source code and title for debugging  
```  
  
---  
  
## Examples  
  
```  
$ gettitle "https://blog.m157q.tw"  
  
Home | Just for noting  
https://blog.m157q.tw/  
```  
  
```  
$ gettitle -m "https://blog.m157q.tw"  
  
[Home | Just for noting](https://blog.m157q.tw/)  
```  
  
---  
  
## Testing  
  
`$ python -m unittest`  
