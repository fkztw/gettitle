# Gettitle  
  
A Python 3 script depends on [robobrowser](https://github.com/jmcarp/robobrowser) and [dryscrape](https://github.com/niklasb/dryscrape) to grab the title of webpage (even the webpages use JavaScript).  
Can print out in normal or markdown format.  
Currently support auto copy to clipboard via `xclip`.  
  
---  
  
## Installation  
  
`$ pip install git+https://github.com/M157q/gettitle`  
  
## Usage  
  
```  
usage: gettitle.py [-h] [-m] [-d] url [url ...]  
  
positional arguments:  
  url             url(s) of the webpage  
  
optional arguments:  
  -h, --help      show this help message and exit  
  -m, --markdown  output with markdown format  
  -d, --debug     print out webpage source code and title for debugging  
```  
